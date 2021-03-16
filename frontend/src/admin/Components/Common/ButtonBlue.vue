<template>
  <button class="blueBtn">{{ word }}</button>
</template>

<script>
export default {
  name: 'ButtonBlue',
  props: ['word']
}
</script>

<style scoped lang="scss">
.blueBtn {
  width: 60px;
  height: 30px;
  border: none;
  border-top-left-radius: 5px;
  border-bottom-left-radius: 5px;
  background-color: #5bc0de;
  color: white;
  font-family: Verdana, sans-serif;
  font-size: 14px;

  &:hover {
    background-color: #4bb8d6;
  }
}
</style>
