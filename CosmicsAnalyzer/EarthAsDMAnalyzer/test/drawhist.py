import ROOT as r
import argparse

def loadTree(file_path, tree_name):
    tree = r.TChain(tree_name)
    tree.Add(file_path)
    return tree

def drawHist(hist, x_label, save_path, color, title, draw_option="HIST", legend_label=""):



    r.gStyle.SetOptStat(0)
    hist.Draw(draw_option)
    hist.SetLineColor(color)
    hist.SetLineWidth(2)
    hist.GetXaxis().SetTitle(x_label)
    hist.GetYaxis().SetTitle("Events")
    hist.SetTitle(title)

    # if legend_label:
    #     legend = r.TLegend(0.7, 0.75, 0.9, 0.9)
    #     legend.AddEntry(hist, legend_label, "l")
    #     legend.Draw()

    return hist

def drawCanvas(hist1, hist2, legendItem1, legendItem2, title,x1,x2,y1,y2):

    can = r.TCanvas()
    can.Draw()
    hist1.SetLineColor(r.kRed)
    hist1.Draw()

    hist2.SetLineColor(r.kBlue)
    hist2.Draw("same")

    legend = r.TLegend(x1,x2,y1,y2)  # Define the legend position
    legend.SetFillColor(0)
    legend.SetBorderSize(1)

    legend.AddEntry(hist1, legendItem1, "l")  # Add entry to the legend for the current histogram
    legend.AddEntry(hist2, legendItem2, "l")
    legend.Draw()

    can.SaveAs(f"plots/NoTrigger1Leg/{title}_both.pdf")
    can.SaveAs(f"plots/test7/{title}_both.png")

    return can


def draw2DHist(hist1, legendItem1, legendItem2, title): #x1,x2,y1,y2):

    can = r.TCanvas()
    can.Draw()
    hist1.SetLineColor(r.kRed)
    hist1.Draw("COLZ")

    # hist2.SetLineColor(r.kBlue)
    # hist2.Draw("same")

    legend = r.TLegend(x1,x2,y1,y2)  # Define the legend position
    legend.SetFillColor(0)
    legend.SetBorderSize(1)

    legend.AddEntry(hist1, legendItem1, "l")  # Add entry to the legend for the current histogram
    # legend.AddEntry(hist2, legendItem2, "l")
    legend.Draw()

    can.SaveAs(f"plots/Trigger1Leg/{title}_both.pdf")
    can.SaveAs(f"plots/Trigger1Leg/{title}_both.png")

    return can

def draw2DHistNoLegend(hist1, title): #x1,x2,y1,y2):

    can = r.TCanvas()
    can.Draw()
    hist1.SetLineColor(r.kRed)
    #hist1.SetStats(0);
    hist1.Draw("COLZ")


    can.SaveAs(f"plots/test2/{title}_both.pdf")
    can.SaveAs(f"plots/test2/{title}_both.png")


    # #Making a tprofile
    can2 = r.TProfile("profile", title, 10, -10, 10) #title, x_bins, x_min, x_max)
    can2.Draw() 
    can2.SaveAs(f"plots/test/{title}_both.pdf")
    can2.SaveAs(f"plots/test/{title}_both.png")

    return can


def create_and_save_tprofile(hist2D, title, x_axis_title, y_axis_title):
    # Creating a TProfile
    num_x_bins = hist2D.GetNbinsX()
    x_min = hist2D.GetXaxis().GetXmin()
    x_max = hist2D.GetXaxis().GetXmax()
    can2 = r.TProfile(f"profile_{title}", title, num_x_bins, x_min, x_max)

    # Setting axis titles
    can2.GetXaxis().SetTitle(x_axis_title)
    can2.GetYaxis().SetTitle(y_axis_title)

    # Loop through the bins and fill the TProfile with mean values
    for i in range(1, num_x_bins + 1):
        bin_content_0 = hist2D.GetBinContent(i, 1)
        bin_content_1 = hist2D.GetBinContent(i, 2)
        mean_value = (bin_content_0 + bin_content_1) / 2.0
        can2.Fill(hist2D.GetXaxis().GetBinCenter(i), mean_value)

    # Drawing the TProfile
    can2.Draw()

    # Saving the TProfile as PDF and PNG files
    can2.SaveAs(f"plots/test/{title}_both.pdf")
    can2.SaveAs(f"plots/test/{title}_both.png")

    return can2




def main():

    # Load first tree
    #tree1 = loadTree("MCntuple0to75-10000Events.root", "muonPhiAnalyzer/tree")
    tree1 = loadTree("MCntuple-0to75-splitMuons-3Triggers-WithEnergy.root", "muonPhiAnalyzer/tree")
    nevents1 = tree1.GetEntries()
    print("nentries1 = ", nevents1)
    
    # Load second tree
    #tree2 = loadTree("MCntuple91to180-10000Events.root", "muonPhiAnalyzer/tree")
    tree2 = loadTree("MCntuple-91to180-splitMuons-3Triggers-WithEnergy.root", "muonPhiAnalyzer/tree") 
    nevents2 = tree2.GetEntries()
    print("nentries2 = ", nevents2)

    h_muonPhi1 = r.TH1F("h_muonPhi1", "Muon #Phi Comparison;#phi;yield", 100, -4, 4)
    h_muonPhi2 = r.TH1F("h_muonPhi2", "Muon #phi - 91 to 180;#phi;yield", 100, -4, 4)
    h_muonPt1 = r.TH1F("h_muonPt1", "Muon pT Comparison;pt;yield", 100, 0, 300)
    h_muonPt2 = r.TH1F("h_muonPt2", "Muon pT Comparison;pt;yield", 100, 0, 300)
    h_muonEta1 = r.TH1F("h_muonEta1", "Muon #eta Comparison;#eta;yield", 100, -2.5, 2.5)
    h_muonEta2 = r.TH1F("h_muonEta2", "Muon #eta Comparison;#eta;yield", 100, -2.5, 2.5)
    h_muon_freeInvBeta1 = r.TH1F("h_muon_freeInvBeta1", "Muon FreeInverseBeta Comparison;freeInvBeta;yield", 100, -50, 50)
    h_muon_freeInvBeta2 = r.TH1F("h_muon_freeInvBeta2", "Muon FreeInverseBeta Comparison;freeInvBeta;yield", 100, -50, 50)
    h_muon_timeAtIpInOut1 = r.TH1F("h_muon_timeAtIpInOut1", "Muon TimeAtIpInOut Comparison;timeAtIpInOut;yield", 100, -500, 500)
    h_muon_timeAtIpInOut2 = r.TH1F("h_muon_timeAtIpInOut2", "Muon TimeAtIpInOut Comparison;timeAtIpInOut;yield", 100, -500, 500)
    h_muon_timeAtIpOutIn1 = r.TH1F("h_muon_timeAtIpOutIn1", "Muon TimeAtIpOutIn Comparison;timeAtIpOutIn;yield", 100, -500, 500)
    h_muon_timeAtIpOutIn2 = r.TH1F("h_muon_timeAtIpOutIn2", "Muon TimeAtIpOutIn Comparison;timeAtIpOutIn;yield", 100, -500, 500)

    h_muonGlobalYvsTime1 = r.TH2D("h_muonGlobalYvsTime1", "Background MC GlobalY vs time;time[ns];GlobalY", 100, -100, 100, 50, -800, 800)
    h_muonGlobalYvsTime2 = r.TH2D("h_muonGlobalYvsTime2", "Signal MC GlobalY vs time;time[ns];GlobalY", 100, -100, 100, 50, -800, 800)

    h_TriggervsEnergy1 = r.TH2D("h_TriggervsEnergy1", "Signal MC trigger vs energy;0 or 1;energy", 100, 0, 2, 50, 0, 2000)
    h_TriggervsEnergy2 = r.TH2D("h_TriggervsEnergy2", "Signal MC trigger vs energy;0 or 1;energy", 100, 0, 2, 50, 0, 2000)

    h_muonEnergy1 = r.TH1F("h_muonEnergy1", "Muon Energy Comparison;energy;yield", 100, -100, 3000)
    h_muonEnergy2 = r.TH1F("h_muonEnergy2", "Muon Energy Comparison;energy;yield", 100, -100, 3000)


    event_count = 0
    pfreq = 1000

    for tree in [tree1, tree2]:
        for event in tree:
            #if event_count % pfreq == 0:
                #print('Processing Event from Tree %d: %d' % (tree, event_count))

            for phi in event.muon_phi:
                if phi > -1000 and phi < 1000: # and event.muon_tofMap_found == 1:
                    if tree == tree1:
                        h_muonPhi1.Fill(phi)
                    else:
                        h_muonPhi2.Fill(phi)

            for pt in event.muon_pt:
                if pt > -1000 and pt < 1000: # and event.muon_tofMap_found == 1:
                    if tree == tree1:
                        h_muonPt1.Fill(pt)
                    else:
                        h_muonPt2.Fill(pt)

            for eta in event.muon_eta:
                if eta > -1000 and eta < 1000: # and event.muon_tofMap_found == 1:
                    if tree == tree1:
                        h_muonEta1.Fill(eta)
                    else:
                        h_muonEta2.Fill(eta)

            for FreeInvBeta in event.muon_comb_freeInvBeta:
                if FreeInvBeta > -1000 and FreeInvBeta < 1000 and FreeInvBeta != 0: #event.muon_tofMap_found == 1:  #and FreeInvBeta !=0:
                        if tree == tree1:
                            h_muon_freeInvBeta1.Fill(FreeInvBeta)
                        else:
                            h_muon_freeInvBeta2.Fill(FreeInvBeta)

            for timeAtIpInOut in event.muon_comb_timeAtIpInOut:
                if timeAtIpInOut > -1000 and timeAtIpInOut < 1000 and timeAtIpInOut != 0: #event.muon_tofMap_found == 1: #and timeAtIpInOut != 0:
                    if tree == tree1:
                        h_muon_timeAtIpInOut1.Fill(timeAtIpInOut)
                    else:
                        h_muon_timeAtIpInOut2.Fill(timeAtIpInOut)

            for timeAtIpOutIn in event.muon_comb_timeAtIpOutIn:
                if timeAtIpOutIn > -1000 and timeAtIpOutIn < 1000 and timeAtIpOutIn != 0: #event.muon_tofMap_found == 1:
                    if tree == tree1:
                        h_muon_timeAtIpOutIn1.Fill(timeAtIpOutIn)
                    else:
                        h_muon_timeAtIpOutIn2.Fill(timeAtIpOutIn)

            # for dtSeg_globY in event.muon_dtSeg_globY:
            #     if dtSeg_globY > -1000 and dtSeg_globY < 1000 and dtSeg_globY != 0: #event.muon_tofMap_found == 1:
            #         if tree == tree1:
            #             h_muonGlobalYvsTime1.Fill(dtSeg_globY)
            #         else:
            #             h_muonGlobalYvsTime1.Fill(dtSeg_globY)
            
            if event.trig_HLT_L1SingleMuCosmics_v2 == 1:

                for (dtSeg_t0timing, dtSeg_globY, dtSeg_found) in zip (event.muon_dtSeg_t0timing, event.muon_dtSeg_globY, event.muon_dtSeg_found):
                    if dtSeg_t0timing > -1000 and dtSeg_t0timing < 1000 and dtSeg_t0timing != 0 and dtSeg_found == 1: #event.muon_tofMap_found == 1:
                        if tree == tree1:
                            h_muonGlobalYvsTime1.Fill(dtSeg_t0timing, dtSeg_globY)
                        else:
                            h_muonGlobalYvsTime2.Fill(dtSeg_t0timing, dtSeg_globY)



#######Created For TProfile

            if event.trig_HLT_L1SingleMuCosmics_v2 == 1:

                for energy in event.muon_energy:
                    if energy > -1000 and energy < 1000: #and dtSeg_t0timing != 0 and dtSeg_found == 1: #event.muon_tofMap_found == 1:
                        if tree == tree1:
                            h_TriggervsEnergy1.Fill(1, energy)
                        else:
                            h_TriggervsEnergy2.Fill(1, energy)

            if event.trig_HLT_L1SingleMuCosmics_v2 == 0:

                for energy in event.muon_energy:
                    if energy > -1000 and energy < 1000: #and dtSeg_t0timing != 0 and dtSeg_found == 1: #event.muon_tofMap_found == 1:
                        if tree == tree1:
                            h_TriggervsEnergy1.Fill(0, energy)
                        else:
                            h_TriggervsEnergy2.Fill(0, energy)


            event_count += 1


    create_and_save_tprofile(h_TriggervsEnergy1, "Trigger1_Profile", "Trigger Value", "Mean Energy")
    create_and_save_tprofile(h_TriggervsEnergy2, "Trigger2_Profile", "Trigger Value", "Mean Energy")


    # drawCanvas(h_muonPhi1,h_muonPhi2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'muonPhi', 0.75, 0.4, 0.95, 0.55)
    # drawCanvas(h_muonPt1,h_muonPt2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'muonPt', 0.75, 0.4, 0.95, 0.55)
    # drawCanvas(h_muonEta1,h_muonEta2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'muonEta', 0.75, 0.4, 0.95, 0.55)
    # drawCanvas(h_muon_freeInvBeta1,h_muon_freeInvBeta2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'muonfreeInvBeta', 0.75, 0.4, 0.95, 0.55)
    # drawCanvas(h_muon_timeAtIpInOut1,h_muon_timeAtIpInOut2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'muontimeAtIpInOut', 0.75, 0.4, 0.95, 0.55)
    # drawCanvas(h_muon_timeAtIpOutIn1,h_muon_timeAtIpOutIn2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'muontimeAtIpOutIn', 0.75, 0.4, 0.95, 0.55)

    # draw2DHistNoLegend(h_muonGlobalYvsTime1, '2Dhist_SplitMuons_0to75_Trigger') #r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', '2Dhisttest') #0.75, 0.4, 0.95, 0.55)
    # draw2DHistNoLegend(h_muonGlobalYvsTime2, '2Dhist_SplitMuons_91to180_Trigger') #r'$91^\circ$ - $180^\circ$', r'$91^\circ$ - $180^\circ$', '2Dhisttest') #0.75, 0.4, 0.95, 0.55)

    # draw2DHistNoLegend(h_TriggervsEnergy1, 'h_TriggervsEnergy1_0to75_Trigger') #r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', '2Dhisttest') #0.75, 0.4, 0.95, 0.55)
    # draw2DHistNoLegend(h_TriggervsEnergy2, 'h_TriggervsEnergy2_91to180_Trigger') #r'$91^\circ$ - $180^\circ$', r'$91^\circ$ - $180^\circ$', '2Dhisttest') #0.75, 0.4, 0.95, 0.55)

    # drawCanvas(h_muon1LegPhi1,h_muon1LegPhi2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'muon1LegPhi', 0.75, 0.4, 0.95, 0.55)
    # drawCanvas(h_muon1LegPt1,h_muon1LegPt2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'muon1LegPt', 0.75, 0.4, 0.95, 0.55)
    # drawCanvas(h_muon1LegEta1,h_muon1LegEta2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'muon1LegEta', 0.75, 0.4, 0.95, 0.55)
    # drawCanvas(h_muon1Leg_freeInvBeta1,h_muon1Leg_freeInvBeta2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'muon1LegfreeInvBeta', 0.75, 0.4, 0.95, 0.55)
    # drawCanvas(h_muon1Leg_timeAtIpInOut1,h_muon1Leg_timeAtIpInOut2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'muon1LegtimeAtIpInOut', 0.75, 0.4, 0.95, 0.55)
    # drawCanvas(h_muon1Leg_timeAtIpOutIn1,h_muon1Leg_timeAtIpOutIn2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'muon1LegtimeAtIpOutIn', 0.75, 0.4, 0.95, 0.55)

    # drawCanvas(h_splitmuonPhi1,h_splitmuonPhi2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'splitmuonPhi', 0.75, 0.4, 0.95, 0.55)
    # drawCanvas(h_splitmuonPt1,h_splitmuonPt2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'splitmuonPt', 0.75, 0.4, 0.95, 0.55)
    # drawCanvas(h_splitmuonEta1,h_splitmuonEta2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'splitmuonEta', 0.75, 0.4, 0.95, 0.55)
    # drawCanvas(h_splitmuon_freeInvBeta1,h_splitmuon_freeInvBeta2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'splitmuon_freeInvBeta', 0.75, 0.4, 0.95, 0.55)
    # drawCanvas(h_splitmuon_timeAtIpInOut1,h_splitmuon_timeAtIpInOut2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'splitmuon_timeAtIpInOut', 0.75, 0.4, 0.95, 0.55)
    # drawCanvas(h_splitmuon_timeAtIpOutIn1,h_splitmuon_timeAtIpOutIn2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'splitmuon_timeAtIpOutIn', 0.75, 0.4, 0.95, 0.55)

    # drawCanvas(h_lhcSTAMuonPhi1,h_lhcSTAMuonPhi2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'lhcSTAMuonPhi', 0.75, 0.4, 0.95, 0.55)
    # drawCanvas(h_lhcSTAMuonPt1,h_lhcSTAMuonPt2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'lhcSTAMuonPt', 0.75, 0.4, 0.95, 0.55)
    # drawCanvas(h_lhcSTAMuonEta1,h_lhcSTAMuonEta2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'lhcSTAMuonEta', 0.75, 0.4, 0.95, 0.55)
 #   drawCanvas(h_lhcSTAMuon_freeInvBeta1,h_lhcSTAMuon_freeInvBeta2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'lhcSTAMuon_freeInvBeta', 0.75, 0.4, 0.95, 0.55)
 #   drawCanvas(h_lhcSTAMuon_timeAtIpInOut1,h_lhcSTAMuon_timeAtIpInOut2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'lhcSTAMuon_timeAtIpInOut', 0.75, 0.4, 0.95, 0.55)
 #   drawCanvas(h_lhcSTAMuon_timeAtIpOutIn1,h_lhcSTAMuon_timeAtIpOutIn2, r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', 'lhcSTAMuon_timeAtIpOutIn', 0.75, 0.4, 0.95, 0.55)




if __name__ == "__main__":
    main()