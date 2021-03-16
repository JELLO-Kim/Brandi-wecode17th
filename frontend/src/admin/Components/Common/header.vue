<template>
  <header>
    <div class="page-logo" @click="toHome">
      <a class="link-home">
        <img alt src="@/assets/images/brandi_logo.png" />
      </a>
    </div>
    <div class="transparent" @mouseover="setMouseOver">
      <div class="logout">
        <span class="username">intern_master</span>
        <i class="fa fa-angle-down" />
        <div
          class="dropdown"
          @mouseover="setMouseOver"
          @mouseleave="resetMouseOver"
          v-if="mouseOn"
          @click="handleLogout"
        >
          <a href="/">
            <i class="fa fa-key" />
            <span>Log out</span>
          </a>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
// import { mapActions } from 'vuex'

export default {
  data () {
    return {
      mouseOn: false
    }
  },
  methods: {
    setMouseOver () {
      this.mouseOn = true
    },
    resetMouseOver () {
      this.mouseOn = false
    },
    toHome () {
      if (this.$router.history.current.path !== '/admin') {
        this.$router.push('/admin')
      }
    },
    handleLogout () {
      // clear()
      this.logout()
      this.$router.push('/')
    }
  }
}
</script>

<style lang="scss" scoped>
header {
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  justify-content: space-between;
  width: 100%;
  height: 45px;
  min-height: 45px;
  border: 0px;
  margin: 0;
  background: #1a1a1a;
  box-shadow: none;
  z-index: 1200;
  font-family: sans-serif;

  .page-logo {
    display: flex;
    align-items: center;
    width: 225px;
    height: 45px;
    padding: 0 20px;
    line-height: 40px;
    cursor: pointer;

    img {
      width: 100px;
    }
  }

  .logout {
    position: relative;
    display: flex;
    align-items: center;
    width: 150px;
    height: 45px;
    padding: 0 10px;
    margin-right: 20px;
    cursor: pointer;

    &:hover {
      background: #414247;
    }

    .transparent {
      position: absolute;
      top: 0;
      width: 100%;
      height: 150px;
    }

    .username {
      color: #cecfd3;
      line-height: 20px;
      margin-right: 5px;
    }

    .fa-angle-down {
      font-family: "FontAwesome";
      font-size: 13px;
      color: #999ba2;

      &:before {
        content: "\f107";
      }
    }

    .dropdown {
      position: absolute;
      display: flex;
      align-items: center;
      top: 45px;
      right: 0;
      left: auto;
      min-width: 160px;
      height: 40px;
      padding: 5px 0;
      border: 1px solid rgba(0, 0, 0, 0.15);
      border-radius: 4px;
      box-shadow: 5px 5px rgba(102, 102, 102, 0.1);
      margin-top: 2px;
      font-size: 14px;
      text-align: left;
      list-style: none;
      background-color: #fff;
      background-clip: padding-box;
      z-index: 1000;

      a {
        clear: both;
        padding: 6px 0 6px 13px;
        color: #333;
        text-decoration: none;
        font-weight: normal;
        line-height: 18px;
        white-space: nowrap;
        outline: none;

        .fa-key {
          margin-right: 12px;
          font-size: 14px;

          &:before {
            content: "\f084";
          }
        }
      }
    }
  }
}
</style>
