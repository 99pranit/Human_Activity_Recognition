import math
def softmax(x):
    m = max(x)
    exps = [math.exp(i - m) for i in x]
    s = sum(exps)
    for idx, _ in enumerate(exps):
        exps[idx] /= s
    return exps
def score(input):
    if input[52] < 0.6042942:
        var0 = 2.9840791
    else:
        var0 = -0.59954596
    if input[40] < 0.5900494:
        if input[201] < 0.31045625:
            var1 = 0.57816446
        else:
            var1 = 0.80711323
    else:
        if input[43] < 0.20183581:
            var1 = -0.5382232
        else:
            var1 = 0.12852103
    if input[40] < 0.5900494:
        var2 = 0.54325
    else:
        if input[277] < 0.65832883:
            var2 = -0.5257825
        else:
            var2 = 0.049478885
    if input[40] < 0.5900494:
        if input[55] < 0.9215475:
            var3 = 0.53046435
        else:
            var3 = 0.16113544
    else:
        if input[207] < 0.5419858:
            var3 = -0.5188137
        else:
            var3 = 0.14040723
    if input[52] < 0.48212978:
        var4 = 0.52282053
    else:
        if input[40] < 0.5900494:
            var4 = 0.10263414
        else:
            var4 = -0.51327944
    if input[52] < 0.48212978:
        var5 = 0.51663685
    else:
        if input[40] < 0.5900494:
            var5 = 0.0772892
        else:
            var5 = -0.50412154
    if input[52] < 0.48212978:
        var6 = 0.50150484
    else:
        if input[79] < 0.035327833:
            var6 = -0.085215025
        else:
            var6 = -0.4769259
    if input[559] < 0.765504:
        if input[52] < 0.6042942:
            var7 = -0.5911914
        else:
            var7 = 2.1056082
    else:
        if input[426] < 0.00174113:
            var7 = 1.6482213
        else:
            var7 = -0.51855385
    if input[129] < 0.07242633:
        if input[451] < 0.44817182:
            var8 = -0.09131445
        else:
            var8 = 0.51756346
    else:
        if input[69] < 0.08722111:
            var8 = 0.15727147
        else:
            var8 = -0.5991179
    if input[429] < 0.061849587:
        if input[57] < 0.000135805:
            var9 = -0.85487753
        else:
            var9 = 0.3135897
    else:
        if input[139] < 0.00761427:
            var9 = 0.47926152
        else:
            var9 = -0.5841643
    if input[129] < 0.06516054:
        if input[88] < 0.009465825:
            var10 = 0.14502555
        else:
            var10 = 0.9756171
    else:
        if input[443] < 0.00646526:
            var10 = -0.9774184
        else:
            var10 = -0.18203002
    if input[382] < 0.002799295:
        if input[490] < 0.00008227:
            var11 = -0.060909063
        else:
            var11 = 0.5994623
    else:
        var11 = -0.55225694
    if input[429] < 0.035459626:
        if input[474] < 0.00008852:
            var12 = -0.16071928
        else:
            var12 = 0.40189096
    else:
        if input[63] < 0.5210747:
            var12 = -0.50442857
        else:
            var12 = 0.49450964
    if input[132] < 0.91963243:
        if input[501] < 0.000022865:
            var13 = -0.7149911
        else:
            var13 = -0.059375715
    else:
        if input[409] < 0.000159665:
            var13 = 0.07661535
        else:
            var13 = 1.020083
    if input[296] < 0.28990194:
        if input[41] < 0.2936198:
            var14 = 2.2721145
        else:
            var14 = -0.1337728
    else:
        if input[38] < 0.66667783:
            var14 = -0.48578328
        else:
            var14 = 0.6585365
    if input[135] < 0.20667882:
        if input[559] < 0.69527113:
            var15 = -0.51219875
        else:
            var15 = 0.792398
    else:
        if input[296] < 0.28990194:
            var15 = -0.9062131
        else:
            var15 = -0.5388822
    if input[138] < 0.025155194:
        if input[54] < 0.5928422:
            var16 = 0.48874754
        else:
            var16 = -0.46541297
    else:
        if input[76] < 0.9872697:
            var16 = -0.5501699
        else:
            var16 = 0.41665652
    if input[135] < 0.20667882:
        if input[451] < 0.43698782:
            var17 = 0.5328135
        else:
            var17 = -0.14368431
    else:
        if input[194] < 0.38187483:
            var17 = -0.061382644
        else:
            var17 = -0.53906
    if input[490] < 0.00008227:
        if input[132] < 0.9218497:
            var18 = 0.45397776
        else:
            var18 = -0.4018981
    else:
        if input[64] < 0.12287063:
            var18 = -0.7400786
        else:
            var18 = 0.0042110174
    if input[179] < 0.003321965:
        if input[124] < 0.005212995:
            var19 = 0.09739715
        else:
            var19 = -0.708941
    else:
        if input[105] < 0.5591051:
            var19 = -0.09988304
        else:
            var19 = 0.52807844
    if input[451] < 0.62524647:
        if input[13] < 0.7710822:
            var20 = -0.537983
        else:
            var20 = 0.16656287
    else:
        if input[556] < 0.692043:
            var20 = -0.6634972
        else:
            var20 = 0.49824706
    if input[166] < 0.21650754:
        if input[247] < 0.93390465:
            var21 = -0.57162637
        else:
            var21 = 0.57868016
    else:
        if input[503] < 0.3423511:
            var21 = 2.2089744
        else:
            var21 = -0.35856575
    if input[450] < 0.20833334:
        if input[274] < 0.31270844:
            var22 = -0.22328652
        else:
            var22 = -0.7750824
    else:
        if input[22] < 0.6287221:
            var22 = -0.33023497
        else:
            var22 = 0.8539919
    if input[537] < 0.07692307:
        if input[379] < 0.36276737:
            var23 = -0.49973863
        else:
            var23 = 0.14187272
    else:
        if input[448] < 0.033333335:
            var23 = -0.6083479
        else:
            var23 = 0.53637666
    if input[518] < 0.20637701:
        if input[193] < 0.20112334:
            var24 = 0.29970634
        else:
            var24 = -0.5274339
    else:
        if input[37] < 0.38865:
            var24 = -0.23169173
        else:
            var24 = 0.6396211
    if input[70] < 0.6203701:
        if input[132] < 0.8105701:
            var25 = 0.5330438
        else:
            var25 = -0.4109003
    else:
        if input[37] < 0.42901826:
            var25 = -0.5349418
        else:
            var25 = 0.07960691
    if input[474] < 0.18524785:
        if input[449] < 0.17857143:
            var26 = -0.38960993
        else:
            var26 = 0.22142291
    else:
        if input[198] < 0.6036546:
            var26 = 0.18404849
        else:
            var26 = 0.9845811
    if input[526] < 0.34725904:
        if input[450] < 0.25:
            var27 = -0.5163213
        else:
            var27 = 0.017536443
    else:
        if input[209] < 0.3385389:
            var27 = -0.4599065
        else:
            var27 = 0.3520718
    if input[201] < 0.4854418:
        if input[504] < 0.43510646:
            var28 = -0.5617825
        else:
            var28 = 0.54728216
    else:
        if input[159] < 0.63728654:
            var28 = 2.687657
        else:
            var28 = -0.4883721
    if input[9] < 0.5954711:
        if input[429] < 0.4093257:
            var29 = -0.47041753
        else:
            var29 = 0.8767849
    else:
        if input[418] < 0.02092984:
            var29 = -0.32744533
        else:
            var29 = 0.6797042
    if input[369] < 0.18:
        if input[159] < 0.5969354:
            var30 = 0.59380454
        else:
            var30 = -0.49495792
    else:
        if input[89] < 0.47661355:
            var30 = -0.5214049
        else:
            var30 = 0.51739645
    if input[37] < 0.35558978:
        if input[39] < 0.37066716:
            var31 = 1.5678784
        else:
            var31 = 0.16685943
    else:
        if input[504] < 0.53607416:
            var31 = -0.51226074
        else:
            var31 = 0.40335447
    if input[302] < 0.11033056:
        if input[9] < 0.5994544:
            var32 = -0.5101876
        else:
            var32 = 0.17302041
    else:
        if input[166] < 0.43623355:
            var32 = 0.35004118
        else:
            var32 = -0.7734941
    if input[458] < 0.39711916:
        if input[68] < 0.83741325:
            var33 = -0.48596942
        else:
            var33 = 0.32973284
    else:
        if input[89] < 0.47661355:
            var33 = -0.50488764
        else:
            var33 = 0.3257972
    if input[89] < 0.3623861:
        if input[57] < 0.009850145:
            var34 = 0.41096747
        else:
            var34 = -0.4096404
    else:
        if input[22] < 0.7637757:
            var34 = 0.49461654
        else:
            var34 = -0.5118152
    if input[330] < 0.08699148:
        if input[274] < 0.34396562:
            var35 = -0.5943994
        else:
            var35 = 0.09799786
    else:
        if input[73] < 0.2833298:
            var35 = 2.1551762
        else:
            var35 = -0.25039002
    if input[53] < 0.18150297:
        if input[302] < 0.081044085:
            var36 = -0.535666
        else:
            var36 = 1.2224559
    else:
        if input[374] < 0.40798044:
            var36 = 0.18889955
        else:
            var36 = -0.4838917
    if input[316] < 0.18332888:
        if input[330] < 0.20683502:
            var37 = -0.48385096
        else:
            var37 = 0.17993173
    else:
        if input[450] < 0.16666667:
            var37 = 0.6350389
        else:
            var37 = -0.33145237
    if input[53] < 0.25087455:
        if input[302] < 0.11453215:
            var38 = -0.3238484
        else:
            var38 = 0.5052782
    else:
        if input[51] < 0.3338297:
            var38 = 0.3814161
        else:
            var38 = -0.59430844
    if input[559] < 0.87070477:
        if input[459] < 0.38069195:
            var39 = -0.3194654
        else:
            var39 = 0.32014567
    else:
        if input[89] < 0.42762214:
            var39 = 0.58821416
        else:
            var39 = -0.34206325
    if input[9] < 0.3184109:
        if input[242] < 0.242885:
            var40 = -0.5242613
        else:
            var40 = -0.95734847
    else:
        if input[450] < 0.16666667:
            var40 = 0.33913282
        else:
            var40 = -0.34180018
    if input[274] < 0.29147327:
        if input[293] < 0.23718502:
            var41 = 0.26445928
        else:
            var41 = -0.46677187
    else:
        if input[518] < 0.28151712:
            var41 = 0.4819404
        else:
            var41 = -0.100091286
    return softmax([nan + (var0 + var1 + var2 + var3 + var4 + var5 + var6), nan + (var7 + var8 + var9 + var10 + var11 + var12 + var13), nan + (var14 + var15 + var16 + var17 + var18 + var19 + var20), nan + (var21 + var22 + var23 + var24 + var25 + var26 + var27), nan + (var28 + var29 + var30 + var31 + var32 + var33 + var34), nan + (var35 + var36 + var37 + var38 + var39 + var40 + var41)])
