// pages/testPage/testPage.js
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  // 云函数链接sql，不建议自己调试使用，需要安装依赖环境
  testFunction:function(e) {
    wx.cloud.callFunction({
      name: 'mysql',
      data: {
        database: e.currentTarget.dataset.database,
        instruction: e.currentTarget.dataset.instruction
      },
      success: res => {
        wx.showToast({
          title: '调用成功',
        })
        this.setData({
          result: JSON.stringify(res.result)
        })
      },
      fail: err => {
        wx.showToast({
          icon: 'none',
          title: '调用失败',
        })
        console.error('[云函数] [sum] 调用失败：', err)
      }
    })
  },

  //测试 POST方法获得 服务端 数据
  testRequest:function() {
    var that = this
    wx.request({
      url:'https://reck.sakurasou.life/login/hello', //必填，其他的都可以不填
      header:{  
        'content-type':'application/x-www-form-urlencoded;charset=utf-8',
        'Accept': 'application/json'
      },
      method:'POST',  
      dataType:"json",
      success: function (res){
        console.log(res.data)
          that.setData({
            id: JSON.parse(res.data)['id']
          });
      },
    })
  },

  // 发送图片给服务端
  chooseImage: function(e) {
    var that = this;
    wx.chooseImage({
      count: 1, //默认9张，这里设置三张
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: function(res) {
        wx.showLoading({
          title: '上传中,请稍等...',
        })
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
        var tempFilePaths = res.tempFilePaths;
        //多图片上传，tempFilePaths本地图片地址为一个数组，遍历调用服务器图片上传接口即可实现多图保存
        for (var i = 0; i < tempFilePaths.length; i++) {
        console.log('图片地址名称' + tempFilePaths[i]);
        wx.uploadFile({
        url: "http://127.0.0.1:5000/login/upload", //此处为实际接口地址
        // url: "http://reck.sakurasou.life/login/upload", //此处为实际接口地址
        filePath: tempFilePaths[i], //获取图片路径
        header: {
          'content-type': 'multipart/form-data'
        },
        name: 'upload',
        success: function(res) {
          wx.hideLoading();
          let Result = res.data;
          console.log(Result);//接收返回来的服务器图片地址
          that.setData({
            file_url: Result
          });
        },
          fail: function(res) {
            wx.hideLoading()
            wx.showToast({
              title: '上传失败，请重新上传',
              icon: 'none',
              duration: 2000
              })
            },
        })
        }
        }
        })
    },

    // 测试Post 发送表单给服务端
  testPostdata:function(e) {
    var that = this;
    var fs = wx.getFileSystemManager();
    wx.request({
      url:'http://reck.sakurasou.life/login/login.msg', //必填，其他的都可以不填
      // url:'http://127.0.0.1:5000/login/login.msg', //必填，其他的都可以不填
      header:{  
        'content-type':'application/x-www-form-urlencoded;charset=utf-8',
        'Accept': 'application/json'
      },
      method:'POST',  
      dataType:"json",
      data:{ "id": e.currentTarget.dataset.id,
              "wxid":e.currentTarget.dataset.wxid,
            "type":e.currentTarget.dataset.type,
            "img":fs.readFileSync(img),
          },
      success: function (res){
        console.log(res.data)
          that.setData({
            return_msg: res.data
          });
      },
    })
  },
  
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

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