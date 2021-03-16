<template>
  <agile :autoplay="true">
    <div v-for="(item, index) in imgData" v-bind:key="index">
      <img :src="item" />
    </div>
    <div class="prevBtn" slot="prevButton"></div>
    <div class="nextBtn" slot="nextButton"></div>
  </agile>
</template>
<script>
import imgData from '@/Data/Banner.json'
import { VueAgile } from 'vue-agile'
export default {
  data () {
    return {
      imgData: imgData.data
    }
  },
  components: {
    agile: VueAgile
  }
}
</script>
<style lang="scss" >
.agile {
  width: 100%;
  position: relative;

  img {
    width: 100vw;
  }

  .prevBtn {
    width: 32px;
    height: 32px;
    background-position: 0 0;
    left: 10px;
    top: 200px;
    position: absolute;
    background-image: url(https://www.brandi.co.kr/static/3.49.1/images/controls.png);
  }
  .nextBtn {
    width: 32px;
    height: 32px;
    background-position: -32px 0;
    right: 10px;
    top: 200px;
    position: absolute;
    background-image: url(https://www.brandi.co.kr/static/3.49.1/images/controls.png);
  }
  &__actions {
    margin-top: 20px;
  }
  &__nav-button {
    background: transparent;
    border: none;
    color: #ccc;
    cursor: pointer;
    font-size: 24px;
    transition-duration: 0.3s;
    &:hover {
      color: #888;
    }
  }
  &__dot {
    margin: 0 10px;
    button {
      background-color: black;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: block;
      height: 10px;
      font-size: 0;
      line-height: 0;
      margin: 0;
      padding: 0;
      transition-duration: 0.3s;
      width: 10px;
    }
    &--current,
    &:hover {
      button {
        background-color: #ff204b;
      }
    }
  }
}
</style>
