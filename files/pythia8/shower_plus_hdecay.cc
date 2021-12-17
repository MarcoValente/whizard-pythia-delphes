// main11.cc is a part of the PYTHIA event generator.
// Copyright (C) 2021 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// Keywords: basic usage; LHE file;

// This is a simple test program.
// It illustrates how Les Houches Event File input can be used in Pythia8.
// It uses the ttsample.lhe(.gz) input file, the latter only with 100 events.

#include <iostream>
#include "Pythia8/Pythia.h"
#include "Pythia8Plugins/HepMC2.h"

using namespace Pythia8;

std::string base_name(std::string const & path)
{
  return path.substr(path.find_last_of("/\\") + 1);
}

void findAndReplaceAll(std::string & data, std::string toSearch, std::string replaceStr)
{
    // Get the first occurrence
    size_t pos = data.find(toSearch);
    // Repeat till end is reached
    while( pos != std::string::npos)
    {
        // Replace this occurrence of Sub String
        data.replace(pos, toSearch.size(), replaceStr);
        // Get the next occurrence from the current position
        pos =data.find(toSearch, pos + replaceStr.size());
    }
}

enum HiggsChannel { NONE, bbbb, bbWW, bbgg};
std::map<HiggsChannel, std::string> channel_map = {
  {NONE,"NONE"},
  {bbbb,"bbbb"},
  {bbWW,"bbWW"},
  {bbgg,"bbgg"}
};

int main(int argc, char *argv[]) {

  std::string in_lhe_file    = "";
  std::string out_hepmc_file = "output.hepmc";
  std::string out_lhe_file   = "output.lhe";
  HiggsChannel higgs_channel = NONE;
  bool verbose               = false;

  if(argc >1) { //Find HH channel
    for (std::pair<HiggsChannel, std::string> _p : channel_map) {
      if (_p.second == argv[1]) {
        higgs_channel = _p.first;
        break;
      }
    }
  }
  if(argc >2) in_lhe_file    = std::string(argv[2]);
  if(argc >3) out_hepmc_file = std::string(argv[3]);
  if(argc >4) out_lhe_file   = std::string(argv[4]);

  std::cout << "*********************************************************" << std::endl;
  std::cout << "higgs_channel  = " << channel_map[higgs_channel] << "" << std::endl;
  std::cout << "in_lhe_file    = \"" << in_lhe_file << "\"" << std::endl;
  std::cout << "out_hepmc_file = \"" << out_hepmc_file << "\"" << std::endl;
  std::cout << "out_lhe_file   = \"" << out_lhe_file << "\"" << std::endl;
  std::cout << "verbose        = " << (verbose ? "true" : "false") << "" << std::endl;
  std::cout << "*********************************************************" << std::endl;

  HepMC::Pythia8ToHepMC topHepMC;
  HepMC::IO_GenEvent ascii_io(out_hepmc_file, std::ios::out);

  // Generator. We here stick with default values, but changes
  // could be inserted with readString or readFile.
  Pythia pythia;

  // pythia.readFile("main31.cmnd");

  // Initialize Les Houches Event File run. List initialization information.
  pythia.readString("Beams:frameType = 4");
  pythia.readString("Beams:LHEF = " + in_lhe_file);

  pythia.readString("HardQCD:all = on");
  // pythia.readString("Tune:ee = 7");
  // pythia.readString("Tune:pp = 14");
  // pythia.readString("SpaceShower:rapidityOrder = on");
  // pythia.readString("SigmaProcess:alphaSvalue = 0.140");
  // pythia.readString("SpaceShower:pT0Ref = 1.56");
  // pythia.readString("SpaceShower:pTmaxFudge = 0.91");
  // pythia.readString("SpaceShower:pTdampFudge = 1.05");
  // pythia.readString("SpaceShower:alphaSvalue = 0.127");
  // pythia.readString("TimeShower:alphaSvalue = 0.127");
  // pythia.readString("BeamRemnants:primordialKThard = 1.88");
  // pythia.readString("MultipartonInteractions:pT0Ref = 2.09");
  // pythia.readString("MultipartonInteractions:alphaSvalue = 0.126");
  // pythia.readString("SpaceShower:pTmaxMatch = 2");
  // pythia.readString("TimeShower:pTmaxMatch = 2");
  // pythia.readString("TimeShower:mMaxGamma = 0");

  switch (higgs_channel) {
    case bbbb:
      pythia.readString("25:oneChannel = on 0.5 100 5 -5");
      pythia.readString("25:addChannel = on 0.5 100 5 -5");
      break;
    case bbWW:
      pythia.readString("25:oneChannel = on 0.5 100 5 -5");
      pythia.readString("25:addChannel = on 0.5 100 24 -24");
      break;
    case bbgg:
      pythia.readString("25:oneChannel = on 0.5 100 5 -5");
      pythia.readString("25:addChannel = on 0.5 100 21 21");
      break;
    case NONE:
      break;
  }

  pythia.init();

  // Allow for possibility of a few faulty events.
  int nAbort = 10;
  int iAbort = 0;

    // Create an LHAup object that can access relevant information in pythia.
  LHAupFromPYTHIA8 myLHA(&pythia.process, &pythia.info);
  
  // Open a file on which LHEF events should be stored, and write header.
  myLHA.openLHEF(out_lhe_file);

  // Store initialization info in the LHAup object.
  myLHA.setInit();

  // Write out this initialization info on the file.
  myLHA.initLHEF();

  // Begin event loop; generate until none left in input file.
  for (int iEvent = 0; ; ++iEvent) {

    // Generate events, and check whether generation failed.
    if (!pythia.next()) {

      // If failure because reached end of file then exit event loop.
      if (pythia.info.atEndOfFile()) break;

      // First few failures write off as "acceptable" errors, then quit.
      if (++iAbort < nAbort) continue;
      break;
    }

    if(verbose) { 
      pythia.event.list();
    }

    // Store event info in the LHAup object.
    myLHA.setEvent();

    // Write out this event info on the file.
    // With optional argument (verbose =) false the file is smaller.
    myLHA.eventLHEF();

    
    HepMC::GenEvent* hepmcevt = new HepMC::GenEvent();
    topHepMC.fill_next_event( pythia, hepmcevt );
    ascii_io << hepmcevt;
    if (hepmcevt) { delete hepmcevt; hepmcevt=0;}
    


  // // End of event loop.
  }

  // // Give statistics. Print histogram.
  pythia.stat();
  // cout << nCharged;

  // Update the cross section info based on Monte Carlo integration during run.
  myLHA.updateSigma();

  // Write endtag. Overwrite initialization info with new cross sections.
  myLHA.closeLHEF(true);

  // Done.
  return 0;
}
