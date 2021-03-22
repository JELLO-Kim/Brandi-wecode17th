<template>
  <div class="pagenation">
    <a>&lt;&lt;</a>
    <a>&lt;</a>
    <a class="selected page">1</a>
    <a class="page">2</a>
    <a class="page">3</a>
    <a class="page">4</a>
    <a class="page">5</a>
    <a>></a>
    <a>>></a>
  </div>
</template>

<script>
export default {
  name: 'Pagenation'
}
</script>

<style lang="scss" scoped>
.pagenation {
  display: flex;
  justify-content: center;
  text-align: center;
  margin: 10px 0;
  a {
    display: inline-block;
    width: 40px;
    height: 40px;
    line-height: 40px;
    font-size: 16px;
    color: #999;
    &.page {
      border: 1px solid #CCC;
    }
    &.selected {
      color: #000;
    }
  }
}

</style>
