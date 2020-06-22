// pages/login/login.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    index: -1,
    array: ['老师','学生'],
    showDialog: false,
    message: '',
    agreed: false

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
      console.log('form发生了submit事件，携带数据为：', form_data)
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