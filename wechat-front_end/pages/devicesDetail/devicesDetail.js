// pages/devicesDetail/devicesDetail.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    swiper_height: '100px',
    vertical: false,
    type_info: '',
    subscribe: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let type_id=JSON.parse(options.item);
    //用type_id查找数据：
    let data={type_id: "sais81f0aj1h", type_name:'turtlebot2',imgs:['turtlebot2.png','turtlebot2.0.png','turtlebot2.1.png'],
    cost:'100', cost_factor:'200',description:'TurtleBot is a low-cost, personal robot kit with open-source software. TurtleBot was created at Willow Garage by Melonee Wise and Tully Foote in November 2010.',
    components:[{name:'机体',num:'1'},{name:'充电器',num:'1'},{name:'笔记本电脑',num:'1'}],
    available_num: [{date:'2020-6-20', num:5},{date:'2020-6-21', num:3},{date:'2020-6-22', num:2},{date:'2020-6-23', num:2},
    {date:'2020-6-24', num:3},{date:'2020-6-25', num:2},{date:'2020-6-26', num:5},{date:'2020-6-27', num:7},{date:'2020-6-28', num:8},
    {date:'2020-6-29', num:5},{date:'2020-6-30', num:7},{date:'2020-7-1', num:5},{date:'2020-7-2', num:8},{date:'2020-7-3', num:9},],
    total_num: 10, broken_num: 2}
    var new_ava=[]
    data.available_num.forEach(function(item){
      let new_d=item.date.split('-').slice(1).join('-')
      new_ava.push({date:new_d, num:item.num})
    })
    data.available_num=new_ava
    this.setData({
      type_info:data,
    })
    console.log(data);

    //使用用户id和设备id查询subscribe信息
    subs=false //假装查到了
    this.setData({
      subscribe:subs,
    })
  },

  get_height: function(e){
    var winWid = wx.getSystemInfoSync().windowWidth;         //获取当前屏幕的宽度
    var imgh=e.detail.height;　　　　　　　　　　　　　　　　//图片高度
    var imgw=e.detail.width;
    var swiperH=winWid*imgh/imgw + "px"　　　　　　　　　　//等比设置swiper的高度。  即 屏幕宽度 / swiper高度 = 图片宽度 / 图片高度    ==》swiper高度 = 屏幕宽度 * 图片高度 / 图片宽度
    this.setData({
        swiper_height:swiperH　　　　　　　　//设置高度
    })
  },

  subscribe_device() {
    //把更改同步给数据库！！！
    this.subscribe=true
  },

  borrow () {
    wx.navigateTo({
      url: '../borrow/borrow?item='+JSON.stringify(this.data.type_info)
    })
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})