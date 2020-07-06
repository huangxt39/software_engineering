//app.js
App({
  onLaunch: function () {

    // 登录
    wx.login({
      success: res => {
        console.log("login res: ",res)
        this.globalData.code=res.code
        wx.getSetting({
          success: res => {
            if (res.authSetting['scope.userInfo']) {
              // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
              wx.showLoading({title: '登录中'})
              wx.getUserInfo({
                success: res => {
    
                  var that= this
                  console.log("getUserInfo res:",res)
                  var platUserInfoMap = {}
                  platUserInfoMap["encryptedData"] = res.encryptedData;
                  platUserInfoMap["iv"] = res.iv;
    
                  let data={ platCode: that.globalData.code,
                    platUserInfoMap: platUserInfoMap}
                    console.log(data)
                  wx.request({
                    url:'https://reck.sakurasou.life/wx_login/login', //后端数据接口
                    // url:'http://127.0.0.1:5000/login/login.msg', //必填，其他的都可以不填
                    header:{  
                      'content-type':'application/x-www-form-urlencoded;charset=utf-8',
                      'Accept': 'application/json'
                    },
                    method:'POST',  
                    //dataType:"json",
                    data:{ platCode: that.globalData.code,
                            platUserInfoMap: platUserInfoMap},
                    success: function (res){ //调用成功之后获得的数据在res
                      //console.log("request success: res",res)
                      if (res.data.code==1){
                        that.globalData.userInfo= res.data.result[0]
                        console.log("自动登录",res.data.result[0])
                      }
                      else if (res.data.code==0){
                        that.globalData.has_signed=false
                      }
                      if (that.action) {
                        that.action()
                      }
                    },
                  })
                }
              })
            }
          }
        })
      }
    })
    // 获取用户信息
    
  },
  globalData: {
    code: null,
    userInfo: null,
    has_signed: true,
  }
})