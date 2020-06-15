// pages/record/record.js
import util from './../../utils/util.js';
Page({

  /**
   * 页面的初始数据
   */
  data: {
    typeindex:0,  //排序索引
    userid:'',
    orderlist:[],
    filterid:null,
    // sortid:null,  //排序id
    // sort:[],
    // activitylist:[], //会议室列表列表
    scrolltop:null, //滚动位置
    page: 0,  //分页
    device_img:{
    "turtlebot":"../../images/turtlebot2.png",
    "F550":'../../images/F550.png'
    },
    status_button:{
      "待归还":"确认归还",
      "待领取":"确认领取",
      "审核中":"取消借用",
      "借用中":"预约归还",
      "已归还":"评价",
    }
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
      this.fetchIndexData();
      this.fetchOrderData(this.data.userid);
  },
  fetchIndexData:function(){
    this.setData(
      {
        "filter": [
          {
            "id": 0,
            "title": "全部"
          },
          {
              "id": 1,
              "title": "正在进行"
          },
          {
              "id": 2,
              "title": "已结束"
          }
        ]
      }
    )
  },
  fetchOrderData:function(userid){
    const perpage = 10;
    this.setData({
      page:this.data.page+1
    })
    const page = this.data.page;
    const newlist = [];

    // 获取历史借用记录 - 数据库交互
    for(var i =(page-1)*perpage; i < page*perpage; i++){
      // 以下是模拟获取数据
      newlist.push({
        "id": i+1,
        "orderid": "000000",
        "starttime":"2016/07/12",
        "status": util.getRandomArrayElement(['审核中','待领取','借用中','待归还','已归还']),
        "endtime":"2016/07/22",
        "devices":[
          {"name":'turtlebot', "num":util.getRandomArrayElement([1,2,3,4,5])},
          {"name":'F550', "num":util.getRandomArrayElement([1,2,3,4,5])}
        ]
        // "imgurl":["../../images/turtlebot.png","../../images/F550.png"]
        })
    }
    this.setData({
      orderlist:this.data.orderlist.concat(newlist)
    })
  },

  setFilter:function(e){ //选择排序方式, 在这里需要更新显示的借用记录。
    const d= this.data;
    const dataset = e.currentTarget.dataset;
    this.setData({
      typeindex:dataset.typeindex,
      filterid:dataset.filterid
    })
    console.log('排序方式id：'+this.data.filterid);
  },
  scrollHandle:function(e){
    this.setData({
      scrolltop:e.detail.scrollTop
    })
  },
  goTop:function(){
    this.setData({
      scrolltop:0
    })
  },
  scrollLoading:function(){
    this.fetchOrderData();
  },
  onPullDownRefresh:function(){ //下拉刷新
    this.setData({
      page:0,
      orderlist:[]
    })
    this.fetchOrderData();
    this.fetchIndexData();
    setTimeout(()=>{
      wx.stopPullDownRefresh()
    },1000)
  },

  gotoDamage:function(){
    var id=null;
    wx.navigateTo({
      url: '',
    })
  },
  gotoDetail:function(e){
    var id=null;
    wx.navigateTo({
      url: "../orderdetail/orderdetail?item="+ JSON.stringify(e.currentTarget.dataset.item),
    })
  },
  gotoCheck:function(){
    var id=null;
    wx.navigateTo({
      url: '',
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