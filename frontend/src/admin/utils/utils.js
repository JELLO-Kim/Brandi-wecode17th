// 공통 함수 모음
// vue와 관계 없고 독립적인 함수
export default {
  getOffset (el) {
    let _x = 0
    let _y = 0
    while (el && !isNaN(el.offsetLeft) && !isNaN(el.offsetTop)) {
      _x += el.offsetLeft
      _y += el.offsetTop
      el = el.offsetParent
    }
    return { top: _y, left: _x }
  },
  makeComma (val) {
    if (val === undefined) return '-'
    return String(val).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  }
}
