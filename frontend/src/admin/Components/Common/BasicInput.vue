<template>
  <input type="text" class="basicInput" />
</template>

<script>
// import { mapState, mapActions } from 'vuex';
// const joinStore = 'joinStore';

export default {
  data: function () {
    return {
      valid: false
    }
  },
  $_veeValidate: {
    // value getter
    value () {
      return this.$el.value
    },
    // name getter
    name () {
      return this.name
    }
  },
  props: {
    name: String,
    inputType: String,
    value: {
      type: null,
      default: null
    },
    error: {
      type: String,
      default: null
    }
  },
  mounted () {
    this.$el.value = this.value
  }

  // computed: {
  //   ...mapState(joinStore, ['infoInput']),
  //   infoInputVal() {
  //     return this.infoInput;
  //   }
  // },
  // methods: {
  //   ...mapActions(joinStore, ['postInput']),

  //   // postNewInput(e, inputId) {
  //   //   inputId = this.inputType;
  //   //   this.postInput({
  //   //     [inputId]: e.target.value
  //   //   });
  //   // },

  //   viewData(e) {
  //     e.preventDefault();
  //     console.log(this.props);
  //   }
  // }
  // watch: {
  //   validCheck(val) {
  //     if (0 < val < 5) {
  //       this.valid = true;
  //     } else {
  //       this.validateId();
  //     }
  //   }
  // }
}
</script>
<style scoped lang="scss">
//@import '../styles/_reset.scss';
//@import '../styles/commonD.scss';

.basicInput {
  width: 360px;
  height: 35px;
  margin-bottom: 7px;
  border: 1px solid $midgrey;
  border-radius: 5px;
  background-color: white;
  text-indent: 30px;

  &:focus {
    outline: none;
    border: 1px solid $darkgrey;
  }
}

.input-validation {
  margin-bottom: 15px;
  color: $validred;
  font-size: 12px;
}
</style>
