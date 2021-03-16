<template>
  <div class="spinner-whole">
    <div class="loading-img">
      <img
        src="https://sadmin.brandi.co.kr/include/img/ico_brandi_loading.png"
      />
    </div>
    <div class="background"></div>
  </div>
</template>

<script>
export default {
  name: 'Spinner'
}
</script>

<style>
.spinner-whole {
  position: fixed;
  z-index: 1000;
}

.background {
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
}

.loading-img {
  position: absolute;
  width: 400px;
  height: auto;
  top: 25vw;
  left: 45vw;
  animation-name: fadeOut;
  animation-duration: 0.8s;
  animation-delay: 0.5s;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in;
  animation-direction: alternate;
}

@keyframes fadeOut {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0.3;
    transform: translateY(10px);
  }
}
</style>
