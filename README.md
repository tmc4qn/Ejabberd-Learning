# Ejabberd
2017年10月來到新東家，很奇妙的碰上我從以前到現在沒有摸過的Ejabberd，也學習到一點點Erlang的基礎，我相信很少人聽過Ejabberd這個IM(Instant Message)框架，但我相信大家都聽過skype、google hangout、wahtsapp以及facebook的messenger，他們的底層都是從Ejabberd/Erlang來的，究竟ejabberd是什麼？怎麼安裝？以及怎麼修改它的原始碼，我會一個一個慢慢的介紹，在介紹之前先來講ejabberd的小故事。  
Ejabberd目前是可擴展/延伸的Jabber/XMPP伺服器，而E代表Erlang的意思;它支持多個伺服器，並且具有容錯處理，單台伺服器失效不影響整個cluster運作，而把ejabberd發揮得淋漓盡致的人我想whatsapp可以算是箇中翹楚，畢竟當初facebook也是花了190億美元收購whatsapp。

# whatsapp服務端架構
* 幾乎全部使用Erlang
* ejabberd (做了大量改造，使用自己的協議替代XMPP)
* database是Mnesia
* 非常重視性能監控

據說Facebook該開始也想要使用Erlang，但是由於優秀的Erlang工程師太難找而放棄了(有待考證)。

# 目的
由於Ejabberd在網路上的教學資源相較於其他語言(框架)並不多，入門有一定程度的門檻，有鑑於此想撰寫這篇文章來介紹修改Ejabberd的一些思路，廢話不多說就直接開始吧

# 安裝
```
git clone https://github.com/processone/ejabberd.git
```
接著cd到ejabberd專案，然後
```
./autogen.sh
```
這時候腳本會幫你檢查很多東西，會出現以下的訊息
![Imgur Image](https://i.imgur.com/ZpGpcfK.png)

# ref
[Facebook 收購 Whatsapp：晚一步，就得付出巨大代價](http://technews.tw/2014/02/20/facebook-mobile-platform-strategy/)
[WhatsApp 的一点分析](https://blog.caoyue.me/post/whatsapp-and-erlang)  
[Ejabberd XMPP client iOS - Logic behind WhatsApp](https://www.youtube.com/watch?v=Vb0t8WlgBVE)  
[如何学习XMPP协议](https://www.jianshu.com/p/37296f6ef09f)

