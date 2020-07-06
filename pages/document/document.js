// pages/document/document.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    late: true,
    early_text: '#606266',
    late_text: '#2699FB',
    activated_col: '#2699FB',
    deactivated_col: '#909399',
    not_start_color: '#606266',
    on_going_color: '#606266',
    has_ended_color: '#606266',
    now_active: 3, //0:未开始 1：进行中 2：已结束
    docs:[{order_id:'k9yb56vams81nd', name: 'turtlebot2', num: 2, im:'../../images/turtlebot2.png', status:'未开始', start_time:'2020-6-30', end_time:'2020-7-3'},
          {order_id:'i81hem7u1ndka9', name: 'turtlebot2', num: 3, im:'../../images/turtlebot2.png', status:'待领取', start_time:'2020-6-23', end_time:'2020-6-27'},
          {order_id:'01kmxmzbdgd727', name: 'turtlebot2', num: 1, im:'../../images/turtlebot2.png', status:'未归还', start_time:'2020-6-12', end_time:'2020-6-29'},
          {order_id:'1nd791bdbds6zu', name: 'turtlebot2', num: 1, im:'../../images/turtlebot2.png', status:'已逾期', start_time:'2020-5-31', end_time:'2020-6-20'},
          {order_id:'01kzpalm17dyna', name: 'turtlebot2', num: 2, im:'../../images/turtlebot2.png', status:'已结束', start_time:'2020-4-12', end_time:'2020-4-20'}],
    not_start_list:[],
    on_going_list:[],
    has_ended_list: [],
    emergency_list:[],
    now_list:[],
    page_num:0
  },

  not_start() {
    if(this.data.now_active!=0){
      this.setData({
        now_active:0,
        not_start_color: this.data.activated_col,
        on_going_color: this.data.deactivated_col,
        has_ended_color: this.data.deactivated_col,
        now_list: this.data.not_start_list
      })
    }
  },

  on_going() {
    if(this.data.now_active!=1){
      this.setData({
        now_active:1,
        not_start_color: this.data.deactivated_col,
        on_going_color: this.data.activated_col,
        has_ended_color: this.data.deactivated_col,
        now_list: this.data.emergency_list.concat(this.data.on_going_list)
      })
    }
  },

  has_ended() {
    if(this.data.now_active!=2){
      this.setData({
        now_active:2,
        not_start_color: this.data.deactivated_col,
        on_going_color: this.data.deactivated_col,
        has_ended_color: this.data.activated_col,
        now_list: this.data.has_ended_list
      })
    }
  },

  _reverse_lists() {
    var not_start=this.data.not_start_list
    var on_going=this.data.on_going_list
    var has_ended=this.data.has_ended_list
    var emergency=this.data.emergency_list
    var now
    not_start.reverse()
    on_going.reverse()
    has_ended.reverse()
    emergency.reverse()
    if (this.data.now_active==0){now=not_start}
    else if (this.data.now_active==1){now=emergency.concat(on_going)}
    else if (this.data.now_active==2){now=has_ended}
    this.setData({
      not_start_list:not_start,
      on_going_list:on_going,
      has_ended_list: has_ended,
      emergency_list: emergency,
      now_list: now
    })
  },

  select_early() {
    if(this.data.late){
      this.setData({
        late: false,
        late_text: '#606266',
        early_text: '#2699FB',
      })
      this._reverse_lists()
    }
  },

  select_late() {
    if(!this.data.late){
      this.setData({
        late: true,
        early_text: '#606266',
        late_text: '#2699FB',
      })
      this._reverse_lists()
    }
  },

  _value_function( a,b ) {
    var a_time=[]
    var b_time=[]
    a.start_time.split('-').forEach((value)=>{a_time.push(parseInt(value))})
    b.start_time.split('-').forEach((value)=>{b_time.push(parseInt(value))})
    if(a[0]==b[0]){
      if(a[1]==b[1]){
        return a[2]-b[2]
      }
      else{ return a[1]-b[1]}
    }
    else {return a[0]-b[0]}
  },

  order_lists() {
    var not_start=[]
    var on_going=[]
    var has_ended=[]
    var emergency=[]
    this.data.docs.forEach(function(item){
      if(item.status=='未开始'){not_start.push(item)}
      else if(item.status=='已结束'){has_ended.push(item)}
      else if(item.status=='已逾期'){emergency.push(item)}
      else {on_going.push(item)}
    })
    not_start.sort(this._value_function)
    on_going.sort(this._value_function)
    has_ended.sort(this._value_function)
    emergency.sort(this._value_function)
    this.setData({
      not_start_list:not_start,
      on_going_list:on_going,
      has_ended_list: has_ended,
      emergency_list: emergency
    })

  },

  get_data(){
    console.log(app.globalData.userInfo)
    wx.showLoading({title: '正在获取'})
    var raw_data
    var that=this
    wx.request({
      url:'https://reck.sakurasou.life/wx_record/get_record', //后端数据接口
      // url:'http://127.0.0.1:5000/login/login.msg', //必填，其他的都可以不填
      header:{  
        'content-type':'application/x-www-form-urlencoded;charset=utf-8',
        'Accept': 'application/json'
      },
      method:'POST',  
      dataType:"json",
      data:{ user_id: app.globalData.userInfo.user_id,
              page: that.data.page_num,
            per_page: 8},
      success: function (res){ //调用成功之后获得的数据在res
        console.log(res.data.code)
        if (res.data.code==1){
          raw_data=res.data.result
          console.log("获取的数据",res.data.result)
          wx.hideLoading({})
        }
        else {
          wx.showToast({title:"获取记录失败",icon:"none"})
        }
      },
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.get_data()
    this.order_lists()
    this.on_going()
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