from src.utils.ps_parser import sql_ps_player_parser

player_details = '{"!Fireredkomodo":{"username":"fireredkomodo","userid":"fireredkomodo","registertime":1476144000,"group":1,"ratings":{"anythinggoes":{"elo":1000,"gxe":41.5,"rpr":1431.7243068961,"rprd":124.10395154732},"gen7anythinggoesbeta":{"elo":1000,"gxe":45,"rpr":1459.8393856612,"rprd":122.8583080769},"gen7pokebankdoublesou":{"elo":1040,"gxe":50.5,"rpr":1504.0663904092,"rprd":122.56948068408},"gen9doublesou":{"elo":1105.4298053220225,"gxe":57.3,"rpr":1558.4899568390813,"rprd":114.8827938352332},"gen9nationaldexmonotype":{"elo":1101.9521666146156,"gxe":39.1,"rpr":1414.9185557578319,"rprd":71.02983524840047},"gen9ou":{"elo":1015.7640716431332,"gxe":35.4,"rpr":1380.1695559697055,"rprd":121.29595086266745},"gen9vgc2023series1":{"elo":1034.3547117352,"gxe":37.5,"rpr":1399.3050302867,"rprd":102.99986255485},"hackmonscup":{"elo":1040,"gxe":55,"rpr":1540.1606143388,"rprd":122.8583080769},"ou":{"elo":1079.3793664265,"gxe":39.6,"rpr":1417.8709767409,"rprd":84.499771423101},"ubers":{"elo":1100.358705474,"gxe":62.3,"rpr":1599.2675350834,"rprd":111.51861011339}}}}'


def sql_ps_player_parser_test():
    sql_ps_player_parser(player_details)


def main():
    sql_ps_player_parser_test()


if __name__ == '__main__':
    main()
