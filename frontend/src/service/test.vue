<template>
  <div>
      <button @click="btn">뭐지?</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  methods: {
    btn () {
      axios.get('192.168.40.105:5000/main')
        .then(() => {
          alert('성공했다!!!')
        })
        .catch(() => {
          alert('실패했다!!!')
        })
    }
  }
}
</script>

<style>

</style>
