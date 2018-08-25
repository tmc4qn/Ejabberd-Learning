# Ejabberd
2017年10月來到新東家，很奇妙的碰上我從以前到現在沒有摸過的Ejabberd，也學習到一點Erlang的基礎，我相信很少人聽過Ejabberd這個IM(Instant Message)框架，但我相信大家都聽過skype、google hangout、wahtsapp以及facebook的messenger，他們的底層都是從Ejabberd/Erlang來的，究竟Ejabberd是什麼？怎麼安裝？以及怎麼修改它的原始碼，我會一個一個慢慢的介紹，在介紹之前先來講ejabberd的小故事。  
Ejabberd目前是可擴展/延伸的Jabber/XMPP伺服器，而E代表Erlang的意思;它支持多個伺服器，並且具有容錯處理，單台伺服器失效不影響整個cluster運作，而把ejabberd發揮得淋漓盡致的人我想whatsapp可以算是箇中翹楚，畢竟當初facebook也是花了190億美元收購whatsapp。

# whatsapp服務端架構
* 幾乎全部使用Erlang
* ejabberd (做了大量改造，使用自己的協議替代XMPP)
* database是Mnesia
* 非常重視性能監控

據說Facebook該開始也想要使用Erlang，但是由於優秀的Erlang工程師太難找而放棄了(有待考證)。

# 目的
由於Ejabberd在網路上的教學資源相較於其他語言(框架)並不多，入門有一定程度的門檻，有鑑於此想撰寫這篇文章來介紹修改Ejabberd的一些思路，廢話不多說就直接開始吧。Ejabberd除了可以當作IM server外，也可以把它利用在IOT傳訊息的使用上，只要是訊息溝通的用途都可以利用Ejabberd幫你完成。

# 安裝
```
git clone https://github.com/processone/ejabberd.git
```
接著cd到ejabberd專案，然後
```
./autogen.sh
```
之後會產生configure，再下
```
./configure --enable-mysql
```
這時候腳本會幫你檢查很多東西，會出現以下的訊息
![Imgur Image](https://i.imgur.com/ZpGpcfK.png)
這時候就是依照系統指示安裝缺少的套件像是
* erlang
* libssl-dev
* libexpat1-dev
* libyaml-dev

apt-get install 慢慢安裝就可以了

安裝好之後就下make，之後就是make install就沒問題了，看到以下畫面就是完成Ejabberd的安裝了!!
![Imgur Image](https://i.imgur.com/CKsC6d0.png)

[下一篇:如何執行Ejabberd並利用pidgin進行連線](https://github.com/tmc4qn/Ejabberd-Learning/blob/master/1.%20執行Ejabberd與pidgin連線.md)

# ref
[1. Facebook 收購 Whatsapp：晚一步，就得付出巨大代價](http://technews.tw/2014/02/20/facebook-mobile-platform-strategy/)  
[2. WhatsApp 的一点分析](https://blog.caoyue.me/post/whatsapp-and-erlang)  
[3. Ejabberd XMPP client iOS - Logic behind WhatsApp](https://www.youtube.com/watch?v=Vb0t8WlgBVE)  
[4. 如何学习XMPP协议](https://www.jianshu.com/p/37296f6ef09f)  
[5. Ejabberd github](https://github.com/processone/ejabberd)  
[6. Process One(一些Ejabberd的doc都在這邊)](https://www.process-one.net/en/ejabberd/)  
[7. How to install Ejabberd 18.01 XMPP Server with Mysql on Ubuntu 16.04](https://medium.com/modern-sysadmin/how-to-install-ejabberd-18-01-xmpp-server-with-mysql-on-ubuntu-16-04-f0facededf2e)

