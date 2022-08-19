import treeloop.configtree as ct
import treeloop.configvar as cv
import treeloop.configsel as cs
import logging as log
import uproot as ur
import numpy as np
import awkward as awk
from treeloop import helpers

class looper():
    """
    looper() class description
    
    Attributes:
        - tree_name: name of tree to loop on.
        - input_files: list of input root files containing tree.
        - scales: list of of scale factors for each file (e.g. luminosities).
        - branches: branches to read from tree (default: confitree.default_branches)
    """
    def __init__(self,
                 tree_name,
                 input_files,
                 isData=False,
                 aliases=None,
                 scales=None,
                 branches=ct.default_branches,
                 trigger_tree_name='triggerList',
                 trig_expr=None,
                ):
        self.tree_name         = tree_name
        self.input_files       = list(input_files)
        self.scales            = scales
        self.aliases           = aliases
        self.branches          = branches
        self.trigger_tree_name = trigger_tree_name
        self.isData            = isData
        self.trig_expr         = trig_expr
        
        self.checkOptions()
    
    def checkOptions(self):
        self.checkScales()

    def checkScales(self):
        if self.scales:
            if len(self.scales)!=len(self.input_files):
                log.warning('Length of input_files and scales does not match')

    @property
    def addTriggers(self):
        return False if (self.trig_expr is None or self.trig_expr=='') else True

    @property
    def files(self):
        return [ur.open(fn) for fn in self.input_files]
    
    @property
    def trees(self):
        return [f[self.tree_name] for f in self.files]

    def addDataMCFlags(self,event):
        event['isData'] = self.isData
        event['isMC']   = not self.isData

    def addVariablesToEvent(self,event):
        self.addDataMCFlags(event)
        if self.addTriggers:
            self.appendTriggers(event)
    
    def appendTriggers(self,event):
        event['trigger_names'] = []
        event['trigger_passed'] = []

        trig_rnums  = ur.tree.lazyarray(self.input_files,self.trigger_tree_name,'runNumber')
        trig_enums  = ur.tree.lazyarray(self.input_files,self.trigger_tree_name,'eventNumber')
        trig_string = ur.tree.lazyarray(self.input_files,self.trigger_tree_name,'triggerMap.first')
        trig_double = ur.tree.lazyarray(self.input_files,self.trigger_tree_name,'triggerMap.second')

        log.warning('Hacking trigger tree matching since run numbers do not match for MC.')
        for rnum,enm in zip(event['run_number'],event['event_number']):
            # index_list = np.where((trig_enums==enm) * (trig_rnums==rnum))[0]
            index_list = np.where((trig_enums==enm))[0]
            if len(index_list)>0: #A valid matched event was found in trigger_tree
                i = index_list[0]
                log.debug('Found event {0} at position {1} with value {2}'.format(enm,i,trig_enums[i]))
                event['trigger_names'].append(trig_string[i])
                event['trigger_passed'].append(trig_double[i])
            else:
                log.warning(f'Impossible to find triggers for event (rnum,enum)=({rnum},{enum}).')
    
    def addSelectionToEvent(self,event,sel,name):
        event[name] = sel(event,trig_expr=self.trig_expr if self.addTriggers else '')

    def _get(self,updateFunction,variable,*args,selection=cs.baseline,weight=None,**kwargs):
        import concurrent.futures
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

        gen = ur.iterate(
                {f:self.tree_name for f in self.input_files},
                self.branches,
                aliases=self.aliases,
        )

        values=[]
        for file_index,event in enumerate(gen):
            log.info('Looping on file {0} named \'{1}\''.format(file_index,self.input_files[file_index]))
            self.addVariablesToEvent(event)
            self.addSelectionToEvent(event,selection,selection.__name__)
            
            scale=self.scales[file_index] if self.scales else 1.0
            log.info(f'Applying scale {scale}')
            updateFunction(event,variable,values,*args,weight=weight,sel_name=selection.__name__,scale=scale,**kwargs)

        return values
        
    def _updateCount(self, event, variable, values ,*args, weight=None, sel_name=None, scale=1.0, **kwargs):
        v = variable(event,sel_name=sel_name)
        w = np.ones_like(v) if weight is None else weight(event,sel_name=sel_name,lumi=scale)
        # if weight is None:
        #     w = np.ones_like(v) if sel_name is None else np.ones_like(v)[event[sel_name]]
        # else:
        #     w=weight(event,sel_name=sel_name,lumi=scale)
        
        counts=np.sum(w)
        if len(values)==0:
            values.append(counts)
        else:
            values[0] = values[0]+counts

    def _updateVariable(self, event, variable, values ,*args, weight=None, sel_name=None, scale=1.0, **kwargs):
        v = variable(event,sel_name=sel_name)
        w = np.ones_like(v) if weight is None else weight(event,sel_name=sel_name,lumi=scale)
        
        if len(values)==0:
            values.append(v)
        else:
            values[0]+=v
        if len(values)==1:
            values.append(w)
        else:
            values[1]+=w

    def _updateVariables(self, event, vars_dict, values ,*args, weight=None, sel_name=None, scale=1.0, **kwargs):
        if len(values)==0:
            values.append({vname:[] for vname,_ in vars_dict.items()})

        vdict=values[0]
        
        for vname,var in vars_dict.items():
            #Using standard function now
            self._updateVariable(event, var, vdict[vname] ,*args, weight=weight, sel_name=sel_name, scale=scale, **kwargs)

    def _updateHist(self, event, variable, values ,*args, weight=None, sel_name=None, scale=1.0, **kwargs):
        v = awk.flatten(variable(event,sel_name=sel_name),axis=None)
        w = awk.flatten(awk.ones_like(v) if weight is None else weight(event,sel_name=sel_name,lumi=scale),axis=None)
        counts, edges = np.histogram(v,
                                    weights=w,
                                    **kwargs
        )
        errors = helpers.getHistErrors(edges,v,w)
        if len(values)==0:
            values.append(counts)
            values.append(edges)
            values.append(errors)
        else:
            values[0] = values[0]+counts
            values[1] = edges
            values[2] = np.sqrt(values[2]**2+errors**2)

    def _updateHist2d(self, event, variable, values ,*args, weight=None, sel_name=None, scale=1.0, **kwargs):
        v1 = variable[0](event,sel_name=sel_name)
        v2 = variable[1](event,sel_name=sel_name)
        w = np.ones_like(v) if weight is None else weight(event,sel_name=sel_name,lumi=scale)
        counts, xedges, yedges = np.histogram2d(v1,v2,
                                                weights=w,
                                                **kwargs
        )
        if len(values)==0:
            values.append(counts)
            values.append(xedges)
            values.append(yedges)
        else:
            values[0] = values[0]+counts
            values[1] = xedges
            values[2] = yedges

    def getHistogram(self,variable,*args,selection=cs.baseline,weight=None,**kwargs):
        return self._get(self._updateHist,variable,*args,selection=selection,weight=weight,**kwargs)
    
    def getHistogram2d(self,variable1,variable2,*args,selection=cs.baseline,weight=None,**kwargs):
        return self._get(self._updateHist2d,(variable1,variable2),*args,selection=selection,weight=weight,**kwargs)
    
    def count(self,var,*args,selection=cs.baseline,weight=None,**kwargs):
        return self._get(self._updateCount,var,*args,selection=selection,weight=weight,**kwargs)[0]
    
    def variable(self,var,*args,selection=cs.baseline,weight=None,**kwargs):
        return self._get(self._updateVariable,var,*args,selection=selection,weight=weight,**kwargs)[0]
    
    def variables(self,var_dict,*args,selection=cs.baseline,weight=None,**kwargs):
        return self._get(self._updateVariables,var_dict,*args,selection=selection,weight=weight,**kwargs)[0]
    
    