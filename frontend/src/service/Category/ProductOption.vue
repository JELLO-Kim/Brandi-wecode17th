<template>
  <div>
    <h2>상품옵션</h2>
    <ul>
      <li>
        <label>
          <CheckBox v-model="testCheck"></CheckBox> &nbsp; 세일
        </label>
      </li>
    </ul>
  </div>
</template>

<script>
import CheckBox from '@/service/Components/CheckBox'

export default {
  name: 'CategoryMain',
  components: {
    CheckBox
  },
  data () {
    return {
      testCheck: false
    }
  }
}
</script>

<style lang="scss" scoped>
  ul, li {
    margin: 0;
    padding: 0;
    list-style: none;
  }
  ul {
    border-top: 1px solid rgb(231, 231, 231);
    overflow: hidden;
  }
  li {
    padding: 15px 10px;
    border-bottom: 1px solid rgb(231, 231, 231);
    font-size: 16px;
    font-weight: 500;
  }
</style>
