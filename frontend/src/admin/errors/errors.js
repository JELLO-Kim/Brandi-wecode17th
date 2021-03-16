export default {
  ExpireTokenException: function (message) {
    this.message = message
    this.name = 'ExpireTokenException'
  },
  TimeoutException: function (message) {
    this.message = message
    this.name = 'TimeoutException'
  }
}
