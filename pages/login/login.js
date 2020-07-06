// pages/login/login.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    index: -1,
    array: ['老师','学生'],
    showDialog: false,
    message: '',
    agreed: false,
    authorized: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    platUserInfoMap:''
  },

  bindPickerChange: function (e) {
    this.setData({
      index: e.detail.value
    })
  },

  formSubmit: function (e) {
    let form_data= e.detail.value
    if (form_data.type==-1 || form_data.email.length==0 || form_data.name.length==0 || form_data.stu_fac_id.length==0 || form_data.phone.length==0){
      this.openDialog("请正确填写每一个选项")
    }
    else if (!this.data.agreed){
      this.openDialog("请先同意用户须知")
    }
    else {
      var that=this
    // var data={ platCode: app.globalData.code, platUserInforMap:that.data.platUserInfoMap,
    //     user_type: that.data.array[parseInt(form_data.type)],
    //     name: form_data.name,
    //     user_id: form_data.stu_fac_id,
    //   email: form_data.email,
    //   phone: form_data.phone}
    //   console.log(data)
      wx.request({
        url:'https://reck.sakurasou.life/wx_login/signup', //后端数据接口
        // url:'http://127.0.0.1:5000/login/login.msg', //必填，其他的都可以不填
        header:{  
          'content-type':'application/x-www-form-urlencoded;charset=utf-8',
          'Accept': 'application/json'
        },
        method:'POST',  
        dataType:"json",
        data:{ platCode: app.globalData.code, platUserInforMap:that.data.platUserInfoMap,
                user_type: that.data.array[parseInt(form_data.type)],
                name: form_data.name,
                user_id: form_data.stu_fac_id,
              email: form_data.email,
            phone: form_data.phone},
        success: function (res){ //调用成功之后获得的数据在res
          console.log(res.data)
            var code=res.data.code
            if (code==1){
              wx.navigateTo({url: "../login.success/login.success",})
              wx.showLoading({title: '登录中',})
              wx.login({
                success: (res) => {
                   app.globalData.code= res.code
                   wx.request({
                    url:'https://reck.sakurasou.life/wx_login/login', //后端数据接口
                    header:{  
                      'content-type':'application/x-www-form-urlencoded;charset=utf-8',
                      'Accept': 'application/json'
                    },
                    method:'POST',  
                    //dataType:"json",
                    data:{ platCode: app.globalData.code,
                            platUserInfoMap: that.data.platUserInfoMap},
                    success: function (res){ //调用成功之后获得的数据在res
                      //console.log("request success: res",res)
                      if (res.data.code==1){
                        app.globalData.userInfo= res.data.result[0]
                        wx.hideLoading({})
                        wx.showToast({ title: '欢迎! '+app.globalData.userInfo.user_name, icon: 'success',})
                        console.log("自动登录",res.data.result[0])
                      }
                      else {wx.showToast({ title: '请重启小程序!',})}
                    }
                  })
                }
              })
                        
            }
            else if (code==2) {
              wx.login({
                success: (res) => {
                console.log("second login res: ",res)
                app.globalData.code=res.code},
              })
              that.openDialog("姓名学号不正确！")
            }
            else if (code==3) {
              wx.login({
                success: (res) => {
                console.log("second login res: ",res)
                app.globalData.code=res.code},
              })
              that.openDialog("姓名学号已被注册！请向管理员申诉")
            }
            else {
              console.log("aaaa")
              wx.showToast({ title: '请重启小程序!',})
            }
        },
      })
      //console.log('form发生了submit事件，携带数据为：', form_data)
      
    }
    
  },

  checkboxChange (e) {
    console.log('chechbox事件，携带数据为：', e.detail.value)
    if (e.detail.value.length==1){
      this.setData({agreed: true})
    }
    else {
      this.setData({agreed: false})
    }
  },

  openDialog(text) {
    this.setData({
      message: text,
      showDialog: true
    })
  },

  tapDialogButton(e) {
    this.setData({
        showDialog: false,
    })
  },

    testPostdata:function(e) {
        var that = this
        
      },
    

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function () {
    var authorized=null
    wx.getSetting({
      success: (res) => { 
        if (res.authSetting['scope.userInfo']){ authorized=true }
        else {authorized=false}
        this.setData({authorized:authorized})
        if (authorized){
          wx.showLoading({title: '登录中'})
          if(app.globalData.userInfo===null && app.globalData.has_signed){ app.action=this.action}
          else { this.action() }
        }
        else if(!this.data.canIUse) {
          // 在没有 open-type=getUserInfo 版本的兼容处理
          wx.getUserInfo({
            success: res => {
              console.log("!!!!!",res)
              this.setData({
                platUserInfoMap:{encryptedData:res.encryptedData, iv:res.iv}
              })
            }
          })
        }
      },
    })
  },
  getUserInfo: function(e) {
    console.log("bindtap: ",e)
    this.setData({
      platUserInfoMap:{encryptedData:e.detail.encryptedData, iv:e.detail.iv},
      authorized:true
    })
  },

  action() {
    wx.hideLoading({})
    if (app.globalData.userInfo) {
      wx.switchTab({url:"../devices/devices"})
      wx.showToast({ title: '欢迎! '+app.globalData.userInfo.user_name, icon: 'success',})
    }
    else { 
      wx.showToast({ title: '请注册'})
      wx.login({
        success: (res) => {
        console.log("second login res: ",res)
        app.globalData.code=res.code},
      })
      wx.getUserInfo({
        success: res => {
          console.log("!!!!!",res)
          this.setData({
            platUserInfoMap:{encryptedData:res.encryptedData, iv:res.iv}
          })
        }
      })
    }
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