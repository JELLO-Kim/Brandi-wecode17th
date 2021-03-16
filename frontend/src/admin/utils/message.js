// 공통 함수 모음
// vue와 관계 없고 독립적인 함수
import { Modal } from 'ant-design-vue'

export default {
  error (message, onOk) {
    Modal.error({
      content: message,
      onOk: onOk
    })
  },
  success (message, onOk) {
    Modal.success({
      content: message,
      onOk: onOk
    })
  }
}
