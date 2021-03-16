<template>
  <button class="redBtn">{{ word }}</button>
</template>

<script>
export default {
  props: ['word'],
  name: 'ButtonRed'
}
</script>

<style scoped lang="scss">
.redBtn {
  width: 60px;
  height: 30px;
  border: none;
  border-top-right-radius: 5px;
  border-bottom-right-radius: 5px;
  background-color: #d9534f;
  color: white;
  font-family: Verdana, sans-serif;
  font-size: 14px;

  &:hover {
    background-color: #d1493f;
  }
}
</style>
