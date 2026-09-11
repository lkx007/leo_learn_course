window.E2_TOPICS = [
{id:"g1", ic:"🐱", name:"图形化编程", src:"建模大赛", about:"先听积木王国，再点题", steps:[
  {type:"say", emoji:"🧩", title:"图形化是什么？", speak:"图形化编程，就是用积木画画一样拼程序。不用打很多字。",
   lines:["积木拼在一起","不用打很多字"]},
  {type:"say", emoji:"🚩", title:"绿旗开始", speak:"绿旗是开始。红圆是停止。积木要从上往下手拉手。",
   lines:["绿旗 = 开始","红圆 = 停止","从上往下做"]},
  {type:"say", emoji:"📦", title:"打包积木", speak:"把常用的一串积木，打包成自制积木。以后想用，叫它一声就行。这就是函数。",
   lines:["自制积木 = 打包好的小工具","可以再叫它来帮忙"]},
  {type:"quiz", speak:"图形化编程常常怎样做？", prompt:"图形化编程常常？",
   options:[{e:"🧩", t:"拼积木", ok:true},{e:"⌨️", t:"打很长的英文", ok:false}], why:"图形化就是拼积木。"},
  {type:"quiz", speak:"自制积木像什么？", prompt:"自制积木像什么？",
   options:[{e:"📦", t:"打包好的小工具", ok:true},{e:"🍪", t:"一块饼干", ok:false}], why:"自制积木就是函数，可以反复用。"},
  {type:"quiz", speak:"绿旗是停止吗？", prompt:"绿旗是停止吗？", tf:true,
   options:[{e:"✅", t:"是停止", ok:false},{e:"🚩", t:"不是，绿旗是开始", ok:true}], why:"绿旗开始，红圆停止。"}
]},
{id:"g2", ic:"⬇️", name:"从上往下做", src:"建模大赛 · 顺序结构", about:"程序像排队", steps:[
  {type:"say", emoji:"🚶", title:"谁先谁后", speak:"积木手拉手，上面的先做，下面的后做。这叫顺序。",
   lines:["上面先","下面后"]},
  {type:"say", emoji:"1️⃣2️⃣3️⃣", title:"先穿衣服", speak:"先穿袜子，再穿鞋子。程序也一样，先开始，再走路，再说你好。",
   lines:["先开始","再做事","最后说完"]},
  {type:"quiz", speak:"积木手拉手，谁先做？", prompt:"谁先做？",
   options:[{e:"⬆️", t:"上面的先做", ok:true},{e:"⬇️", t:"下面的先做", ok:false}], why:"从上往下执行。"},
  {type:"quiz", speak:"可以先说你好，再点绿旗开始吗？", prompt:"能先说话再开始吗？", tf:true,
   options:[{e:"✅", t:"能，倒过来也行", ok:false},{e:"🚩", t:"不行，要先开始", ok:true}], why:"没有开始，后面的积木不会动。"},
  {type:"quiz", speak:"顺序结构就是按排队做事吗？", prompt:"顺序就是排队做事吗？", tf:true,
   options:[{e:"✅", t:"是", ok:true},{e:"❌", t:"不是", ok:false}], why:"一件一件按顺序做。"}
]},
{id:"g3", ic:"❓", name:"如果积木", src:"建模大赛 · 条件判断", about:"对了才做", steps:[
  {type:"say", emoji:"🚪", title:"如果…那么", speak:"如果碰到墙壁，那么就转身。条件成立，才做里面的事。",
   lines:["先问对不对","对了才做"]},
  {type:"say", emoji:"↔️", title:"否则", speak:"如果答对了，说真棒。否则，说再试试。两条路，只走一条。",
   lines:["对了走这条","不对走那条","一次只走一条"]},
  {type:"quiz", speak:"如果积木是干什么的？", prompt:"如果积木是？",
   options:[{e:"❓", t:"先判断，对了才做", ok:true},{e:"🔁", t:"一直重复做", ok:false}], why:"如果是选路，不是转圈。"},
  {type:"quiz", speak:"条件不成立，里面的积木会做吗？", prompt:"条件不对，里面会做吗？",
   options:[{e:"⏭️", t:"跳过，做后面的", ok:true},{e:"💥", t:"程序炸掉", ok:false}], why:"不对就跳过，继续往下。"},
  {type:"quiz", speak:"那么和否则会同时做完吗？", prompt:"那么和否则会同时做吗？", tf:true,
   options:[{e:"✅", t:"会同时做", ok:false},{e:"1️⃣", t:"不会，只走一条", ok:true}], why:"一次只走一条路。"}
]},
{id:"g4", ic:"🔁", name:"再做一遍", src:"建模大赛 · 循环", about:"转圈做事", steps:[
  {type:"say", emoji:"🔁", title:"重复", speak:"橙色积木常常说：再做一遍。拍手十次，就重复十次。",
   lines:["重复 = 再做几遍"]},
  {type:"say", emoji:"🪆", title:"里面还有圈", speak:"外面转三圈。每转一圈，里面拍两下手。这叫圈圈里还有圈圈。",
   lines:["外面做一次","里面可以再做几次"]},
  {type:"quiz", speak:"重复积木常常干什么？", prompt:"重复积木常常？",
   options:[{e:"🔁", t:"再做几遍", ok:true},{e:"❓", t:"只判断一次", ok:false}], why:"循环是重复做。"},
  {type:"quiz", speak:"外面转圈、里面再拍手，可以吗？", prompt:"圈圈里面还能有圈圈吗？", tf:true,
   options:[{e:"✅", t:"可以", ok:true},{e:"❌", t:"不可以", ok:false}], why:"循环里面还可以再放循环。"}
]},
{id:"g5", ic:"👀", name:"侦测小眼睛", src:"建模11-18 · 侦测与感知", about:"碰到、问一问", steps:[
  {type:"say", emoji:"👀", title:"侦测积木", speak:"侦测积木像小眼睛。问：碰到鼠标了吗？碰到颜色了吗？",
   lines:["侦测 = 看一看、问一问"]},
  {type:"say", emoji:"🦇", title:"超声波", speak:"蝙蝠用声音找路。小车找障碍，常常用超声波眼睛。",
   lines:["超声波像蝙蝠","用来看远近"]},
  {type:"say", emoji:"💬", title:"询问并等待", speak:"想知道小朋友叫什么，用询问并等待。回答会记在回答积木里。",
   lines:["先问","再把回答说出来"]},
  {type:"quiz", speak:"碰到鼠标指针，是哪一种积木？", prompt:"碰到鼠标指针是？",
   options:[{e:"👀", t:"侦测积木", ok:true},{e:"⏳", t:"等待两秒", ok:false}], why:"碰到……是侦测。"},
  {type:"quiz", speak:"超声波能看出颜色吗？", prompt:"超声波能看出颜色吗？", tf:true,
   options:[{e:"🎨", t:"能看颜色", ok:false},{e:"📏", t:"不能，它看远近", ok:true}], why:"超声波看距离，不看颜色。"},
  {type:"quiz", speak:"问名字该用什么？", prompt:"问名字常用？",
   options:[{e:"❓", t:"询问并等待", ok:true},{e:"⏰", t:"计时器", ok:false}], why:"询问并等待会记下回答。"}
]},
{id:"g6", ic:"📦", name:"小盒子变量", src:"建模大赛 · 变量", about:"盒子里放数字", steps:[
  {type:"say", emoji:"📦", title:"变量是盒子", speak:"变量像小盒子。盒子有名字，里面可以放数字。分数、步数，都能放进去。",
   lines:["盒子有名字","里面放数字"]},
  {type:"say", emoji:"➕", title:"改盒子", speak:"得分增加一，就是把盒子里的数加一。先放进去，再拿出来用。",
   lines:["先放进盒子","再拿出来用"]},
  {type:"quiz", speak:"变量像什么？", prompt:"变量像什么？",
   options:[{e:"📦", t:"有名字的小盒子", ok:true},{e:"🚩", t:"绿旗", ok:false}], why:"变量是存东西的盒子。"},
  {type:"quiz", speak:"得分加一，是在干什么？", prompt:"得分加一是？",
   options:[{e:"➕", t:"改盒子里的数", ok:true},{e:"🗑️", t:"扔掉积木", ok:false}], why:"修改变量的值。"}
]},
{id:"g7", ic:"🔗", name:"并且或者不是", src:"建模大赛 · 逻辑", about:"两个条件怎么连", steps:[
  {type:"say", emoji:"🤝", title:"并且", speak:"并且，是两个都要对。要有阳光，并且要有水，小苗才高兴。",
   lines:["并且 = 两个都要"]},
  {type:"say", emoji:"🤷", title:"或者", speak:"或者，是有一个对就行。坐车或者走路，都能到家。",
   lines:["或者 = 有一个就行"]},
  {type:"say", emoji:"🚫", title:"不是", speak:"不是，就是反过来。不是红的，就是别的颜色。",
   lines:["不是 = 反过来"]},
  {type:"quiz", speak:"并且是什么意思？", prompt:"并且是？",
   options:[{e:"✌️", t:"两个都要对", ok:true},{e:"1️⃣", t:"有一个就行", ok:false}], why:"并且要两边都成立。"},
  {type:"quiz", speak:"或者要两边都对吗？", prompt:"或者要两边都对吗？", tf:true,
   options:[{e:"✅", t:"要两边都对", ok:false},{e:"1️⃣", t:"有一个对就行", ok:true}], why:"或者只要一个成立。"}
]},
{id:"g8", ic:"➕", name:"数字会算", src:"建模大赛 · 运算符", about:"加一加、减一减", steps:[
  {type:"say", emoji:"➕", title:"加和减", speak:"积木里也可以算数。三加二等于五。五减一等于四。",
   lines:["加会变多","减会变少"]},
  {type:"say", emoji:"⚖️", title:"比一比", speak:"大于就是更大。小于就是更小。等于就是一样。",
   lines:["大于：更大","小于：更小","等于：一样"]},
  {type:"quiz", speak:"三加二常常等于几？", prompt:"三加二等于？",
   options:[{e:"5️⃣", t:"五", ok:true},{e:"1️⃣", t:"一", ok:false}], why:"3+2=5。"},
  {type:"quiz", speak:"大于是更大的意思吗？", prompt:"大于是更大吗？", tf:true,
   options:[{e:"✅", t:"是", ok:true},{e:"❌", t:"不是", ok:false}], why:"大于就是比较大。"}
]},
{id:"g9", ic:"🎈", name:"科学常识加练", src:"建模大赛 · 基础科学", about:"热气球、小船、防锈", steps:[
  {type:"say", emoji:"🎈", title:"热气球", speak:"热气球能上去，因为里面的热空气更轻，会往上跑。",
   lines:["热空气比较轻","所以气球往上"]},
  {type:"say", emoji:"🚢", title:"铁做的船", speak:"铁钉会沉。做成空心大船，排开的水更多，浮力更大，就能浮。",
   lines:["空心船占的水更多","浮力变大"]},
  {type:"say", emoji:"🧴", title:"铁锅抹油", speak:"铁怕水和空气，会生锈。抹油、刷漆，把水和空气挡住。",
   lines:["油和漆挡住水和空气"]},
  {type:"say", emoji:"🧂", title:"醋和小苏打", speak:"白醋加小苏打，常常会冒泡泡。那是气体跑出来。",
   lines:["两种东西一混，冒气泡"]},
  {type:"quiz", speak:"热气球为什么会上去？", prompt:"热气球为什么上去？",
   options:[{e:"🎈", t:"热空气更轻", ok:true},{e:"🧲", t:"磁铁在吸", ok:false}], why:"热空气比冷空气轻。"},
  {type:"quiz", speak:"铁做成船能浮，常常因为什么？", prompt:"铁船能浮因为？",
   options:[{e:"🛟", t:"空心，浮力更大", ok:true},{e:"🪶", t:"铁变成羽毛了", ok:false}], why:"排开的水更多，浮力更大。"},
  {type:"quiz", speak:"铁锅抹油是为了什么？", prompt:"铁锅抹油是为了？",
   options:[{e:"🛡️", t:"挡住水和空气", ok:true},{e:"🍬", t:"变成糖", ok:false}], why:"隔绝水和空气，不容易锈。"}
]},
{id:"g10", ic:"🔬", name:"探究和模型", src:"建模11-18 · 科学探究", about:"简化、试一试、只改一个", steps:[
  {type:"say", emoji:"🧱", title:"模型要简单", speak:"模型会丢掉一些细节，留下最要紧的。这样才好试、好改。",
   lines:["丢掉次要的","留下要紧的"]},
  {type:"say", emoji:"🚩", title:"还要验证", speak:"模型做好了，要点绿旗试。试完才知道像不像真的。",
   lines:["做好了要试","不对就改"]},
  {type:"say", emoji:"1️⃣", title:"只改一个", speak:"想知道阳光重不重要，只改阳光。水和土要一样。",
   lines:["一次只改一个"]},
  {type:"quiz", speak:"模型为什么要简化？", prompt:"模型为什么简化？",
   options:[{e:"🎯", t:"留下要紧的，好试好改", ok:true},{e:"🎨", t:"只为了好看", ok:false}], why:"简化是为了抓住重点。"},
  {type:"quiz", speak:"先做模型，再想方案，对吗？", prompt:"先做模型再想方案吗？", tf:true,
   options:[{e:"✅", t:"对，先做再想", ok:false},{e:"📝", t:"不对，先想再做模型", ok:true}], why:"先有想法，再做模型去试。"}
]},
{id:"g11", ic:"🪆", name:"套娃积木", src:"建模11-18 · 递归", about:"自己叫自己", steps:[
  {type:"say", emoji:"🪆", title:"套娃", speak:"套娃里面还有套娃。自制积木有时会叫自己。这叫递归。小鱼先记住：自己请自己再做一次。",
   lines:["自己叫自己","像套娃"]},
  {type:"say", emoji:"🛑", title:"要有停", speak:"套娃不能没完没了。要有停下的时候，不然会转晕。",
   lines:["要有停止的条件"]},
  {type:"quiz", speak:"递归常常像什么？", prompt:"递归像什么？",
   options:[{e:"🪆", t:"套娃，自己叫自己", ok:true},{e:"🚌", t:"大巴士", ok:false}], why:"递归就是自己再请自己。"},
  {type:"quiz", speak:"递归可以永远不停止吗？", prompt:"递归能永远不停吗？", tf:true,
   options:[{e:"✅", t:"能永远转", ok:false},{e:"🛑", t:"不行，要能停下", ok:true}], why:"没有停止会转个不停。"}
]},
{id:"g12", ic:"🍽️", name:"盘子叠叠乐", src:"建模11-18 · 栈", about:"后放的先拿", steps:[
  {type:"say", emoji:"🍽️", title:"一叠盘子", speak:"盘子叠起来。最后放上去的，最先拿下来。这叫栈。",
   lines:["后放的先拿"]},
  {type:"quiz", speak:"一叠盘子，先拿哪一个？", prompt:"一叠盘子先拿？",
   options:[{e:"🔝", t:"最上面那个", ok:true},{e:"⬇️", t:"最底下那个", ok:false}], why:"栈是后进先出。"},
  {type:"quiz", speak:"栈是后放的先拿吗？", prompt:"栈是后放的先拿吗？", tf:true,
   options:[{e:"✅", t:"是", ok:true},{e:"❌", t:"不是", ok:false}], why:"后进先出。"}
]},
{id:"g13", ic:"📓", name:"名字小本本", src:"建模11-18 · 字典", about:"名字对着东西", steps:[
  {type:"say", emoji:"📓", title:"小本本", speak:"字典像小本本。写着：小猫对应喵，小狗对应汪。用名字找到东西。",
   lines:["名字 → 东西"]},
  {type:"quiz", speak:"字典常常干什么？", prompt:"字典常常？",
   options:[{e:"🔍", t:"用名字找东西", ok:true},{e:"🏃", t:"让人跑步", ok:false}], why:"键对着值。"},
  {type:"quiz", speak:"字典是一叠盘子吗？", prompt:"字典是一叠盘子吗？", tf:true,
   options:[{e:"🍽️", t:"是盘子", ok:false},{e:"📓", t:"不是，是名字小本本", ok:true}], why:"字典用名字对应。"}
]},
{id:"g14", ic:"📋", name:"一排小格子", src:"建模11-18 · 列表", about:"一个一个排好", steps:[
  {type:"say", emoji:"📋", title:"列表", speak:"列表像一排小格子。第一个、第二个、第三个。可以一个一个看过去，这叫遍历。",
   lines:["排成一排","一个一个看"]},
  {type:"quiz", speak:"列表像什么？", prompt:"列表像什么？",
   options:[{e:"📋", t:"一排小格子", ok:true},{e:"🎈", t:"热气球", ok:false}], why:"列表按顺序排。"},
  {type:"quiz", speak:"一个一个看格子，叫遍历吗？", prompt:"一个一个看叫遍历吗？", tf:true,
   options:[{e:"✅", t:"叫", ok:true},{e:"❌", t:"不叫", ok:false}], why:"遍历就是挨个看。"}
]},
{id:"g15", ic:"💧", name:"一层一层找", src:"建模11-18 · 广度优先", about:"先找身边的朋友", steps:[
  {type:"say", emoji:"💧", title:"水波纹", speak:"把小石子丢进水里，波纹一圈一圈往外。找朋友也一样：先找身边的，再找更远的。这叫广度优先。",
   lines:["先找近的","再找远的"]},
  {type:"quiz", speak:"广度优先常常怎样找？", prompt:"广度优先怎样找？",
   options:[{e:"⭕", t:"一圈一圈，先近后远", ok:true},{e:"🕳️", t:"钻进一条路不回头", ok:false}], why:"BFS 先把旁边找完。"},
  {type:"quiz", speak:"先找身边的朋友，再找更远的，对吗？", prompt:"先近后远对吗？", tf:true,
   options:[{e:"✅", t:"对", ok:true},{e:"❌", t:"不对", ok:false}], why:"广度优先就是先近后远。"}
]},
{id:"g16", ic:"🌲", name:"一条路走到底", src:"建模11-18 · 深度优先", about:"走到底再换路", steps:[
  {type:"say", emoji:"🌲", title:"小路", speak:"树林里找路：先选一条，走到头。走不通，再退回来换另一条。这叫深度优先。",
   lines:["一条路走到底","不通就退回来"]},
  {type:"quiz", speak:"深度优先常常怎样找？", prompt:"深度优先怎样找？",
   options:[{e:"➡️", t:"一条路走到头再换", ok:true},{e:"⭕", t:"先把身边一圈找完", ok:false}], why:"DFS 先走深，再回头。"},
  {type:"quiz", speak:"走不通的时候，可以退回来换路吗？", prompt:"走不通能退回来吗？", tf:true,
   options:[{e:"✅", t:"能退回来", ok:true},{e:"❌", t:"不能退", ok:false}], why:"走不通就退回来，再换一条。"}
]}
];
