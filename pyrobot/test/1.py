import wxfunc
s = '''<msg>
    <fromusername>wxid_mp7earq22qtg22</fromusername>
    <scene>0</scene>
    <commenturl></commenturl>
    <appmsg appid="" sdkver="0">
        <title>你好</title>
        <des>提问前先看 FAQ，谢谢！&#x0A;（点我）（点我）&#x0A;不要在群  调戏机器人</des>
        <action>view</action>
        <type>5</type>
        <showtype>0</showtype>
        <content></content>
        <url></url>
        <dataurl></dataurl>
        <lowurl></lowurl>
        <lowdataurl></lowdataurl>
        <recorditem></recorditem>
        <thumburl>https://mmbiz.qpic.cn/mmbiz_jpg/XaSOeHibHicMGE2icmvafjO0q1Tn4iaZ5ZwR2tbwQqeApayUpLXVORCFEDSy3HpFxgnl1T93iaBCXpSubfGeaC18g3A/300?wxtype=jpeg&amp;wxfrom=0</thumburl>
        <messageaction></messageaction>
        <laninfo></laninfo>
        <extinfo></extinfo>
        <sourceusername>gh_75dea2d6c71f</sourceusername>
        <sourcedisplayname>碲矿</sourcedisplayname>
        <commenturl></commenturl>
        <appattach>
            <totallen>0</totallen>
            <attachid></attachid>
            <emoticonmd5></emoticonmd5>
            <fileext>jpg</fileext>
            <cdnthumburl>3057020100044b304902010002047595a1e402032e180202043eeda67c0204664f11db042431383237613764322d643635322d346431332d396663392d6339613364633066353165360204051408030201000405004c4c0a00</cdnthumburl>
            <aeskey>60943b1b5d623a0064bf7d3107046519</aeskey>
            <cdnthumbaeskey>60943b1b5d623a0064bf7d3107046519</cdnthumbaeskey>
            <encryver>1</encryver>
            <cdnthumblength>8027</cdnthumblength>
            <cdnthumbheight>100</cdnthumbheight>
            <cdnthumbwidth>100</cdnthumbwidth>
        </appattach>
        <webviewshared>
            <publisherId></publisherId>
            <publisherReqId>0</publisherReqId>
        </webviewshared>
        <weappinfo>
            <pagepath></pagepath>
            <username></username>
            <appid></appid>
            <appservicetype>0</appservicetype>
        </weappinfo>
        <websearch />
    </appmsg>
    <appinfo>
        <version>1</version>
        <appname>Window wechat</appname>
    </appinfo>
</msg>'''

# wxfunc.SendXmlMsg("45380715750@chatroom", s)
wxfunc.SendFileMsg("filehelper", r"D:\Downloads\0e3661c3cd006cc023b843516cdd12f6.mp4")