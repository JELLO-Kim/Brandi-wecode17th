<template>
  <aside>
    <ul class="main-menus">
      <li class="toggler">
        <i class="toggle" />
      </li>
      <li
        class="main-menu"
        :key="main.name"
        v-for="main of menus"
        @click="changeCurrMain(main.param)"
      >
        <div
          @click="main.param === 'home' ? wClick(main.url) : ''"
          :class="[
            'main-link',
            main.param === mainMenu && 'active',
            main.param === checkedMenu && 'checked'
          ]"
        >
          <div>
            <i :class="[main.param]" />
            <span class="name">{{ main.name }}</span>
          </div>
          <div>
            <i class="arrow" />
          </div>
        </div>
        <ul :class="['sub-menus', main.param !== checkedMenu && 'hidden']">
          <li
            class="sub-menu"
            :key="sub.name"
            v-for="sub of main.sub"
            @click="changeCurrSub(sub.param)"
          >
            <div
              @click="wClick(sub.url)"
              :class="['sub-link', sub.param === subMenu && 'active']"
            >{{ sub.name }}</div>
          </li>
        </ul>
      </li>
    </ul>
  </aside>
</template>

<script>
import menus from '@/assets/data/aside'
export default {
  data () {
    return {
      menus,
      checkedMenu: this.$route.params.mainMenu
        ? this.$route.params.mainMenu
        : '',
      subMenu: this.$route.params.subMenu
    }
  },
  computed: {
    mainMenu () {
      return this.$route.params.mainMenu ? this.$route.params.mainMenu : ''
    }
  },
  methods: {
    wClick (url) {
      if (this.$router.history.current.path !== `/${url}`) {
        this.$router.push(`/${url}`)
      }
    },
    changeCurrMain (main) {
      this.checkedMenu = this.checkedMenu === main ? '' : main
      // if (this.checkedMenu === "home") {
      //   this.checkedMenu = "";
      //   window.location.reload();
      // }
    },
    changeCurrSub (sub) {
      this.subMenu = sub
      this.changeCurrMain(this.mainMenu)
    },
    toggleFold () {
      this.fold = !this.fold
    }
  },
  mounted () {
    this.checkedMenu = this.$route.params.mainMenu
      ? this.$route.params.mainMenu
      : ''
    this.subMenu = this.$route.params.subMenu
  }
}
</script>

<style lang="scss" scoped>
aside {
  position: fixed;
  top: 45px;
  left: 0;
  width: 215px;
  height: 100%;
  background: #35363a;

  .main-menus {
    list-style-type: none;
    padding-left: 0;
    .toggler {
      border-bottom: 1px solid transparent;

      .toggle {
        float: right;
        width: 25px;
        height: 30px;
        margin: 15px 0;
        border-radius: 4px 0px 0px 4px;
        background-color: #fcfcfc;
        cursor: pointer;

        &:before {
          margin: 0px 2px 3px 8px;
          display: inline-block;
          font-size: 18px;
          font-family: FontAwesome;
          content: "\f104";
          font-weight: 200;
          line-height: 30px;
          text-shadow: none;
        }
      }

      &:after {
        content: "";
        display: table;
        clear: both;
      }
    }

    .main-menu {
      border-bottom: 1px solid #414247;

      &:last-child {
        border-bottom: 0;
      }

      .main-link {
        display: flex;
        justify-content: space-between;
        padding: 10px 13px 10px 15px;
        margin: 0;
        font-family: "Open Sans", sans-serif;
        font-size: 15px;
        font-weight: 100;
        text-decoration: none;
        cursor: pointer;
        color: #eee;

        &:hover {
          color: #f1f1f1;
          background: #27272b;
        }

        &.active {
          border-right: 4px solid #d12610;
          color: #f1f1f1;
          background: #27272b;
        }

        &.checked {
          background: #27272b;

          .arrow {
            &:before {
              content: "\f107";
            }
          }
        }

        i {
          width: 1.25em;
          margin-top: 1px;
          margin-right: 5px;
          color: #999;
          font-size: 16px;
          text-shadow: none;
          font-family: "Simple-Line-Icons";
        }
        .home {
          &:before {
            content: "\e069";
          }
        }
        .order {
          &:before {
            content: "\e04d";
          }
        }
        .refund_order {
          &:before {
            content: "\e04e";
          }
        }
        .product {
          &:before {
            content: "\e035";
          }
        }
        .inquiry {
          &:before {
            content: "\e021";
          }
        }
        .account {
          &:before {
            content: "\e005";
          }
        }
        .promotion {
          &:before {
            content: "\e02f";
          }
        }

        .name {
          font-size: 14px;
        }

        .open {
          &:before {
            font-family: "FontAwesome";
            content: "\f107";
          }
        }

        .arrow {
          transition: all 1.2s ease-in-out;

          &:before {
            font-family: "FontAwesome";
            content: "\f104";
          }
        }
      }

      .sub-menus {
        overflow: hidden;
        padding-left: 0;

        &.hidden {
          margin: 0px;

          .sub-menu {
            height: 0px;
          }
        }

        .sub-menu {
          display: flex;
          align-items: center;
          height: 40px;
          transition: height 0.3s ease;

          &:hover {
            color: #fff;
            background: #414247;
          }

          .sub-link {
            display: flex;
            align-items: center;
            width: 100%;
            padding: 8px 0px 8px 35px;
            text-decoration: none;
            font-size: 14px;
            font-weight: 300;
            background: none;
            margin: 0;
            font-family: "Open Sans", sans-serif;
            text-decoration: none;
            cursor: pointer;
            color: #eee;

            &.active {
              height: 40px;
              color: #fff;
              background: #414247;
            }
          }
        }
      }
    }
  }
}
</style>
