<template>
  <div>
    <label>
      <input
        type="radio"
        :checked="label === 1"
        :name="name"
        :value="label"
        @change="handleValue"
      />
      {{ buttonName }}
    </label>
  </div>
</template>
<script>
export default {
  name: 'RadioBtn',
  props: ['name', 'buttonName', 'label'],
  methods: {
    handleValue () {
      this.$emit('change', this.label)
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/styles/commonD.scss';

label {
  margin-right: 30px;
}

input[type='radio'] {
  width: 13px;
  height: 13px;
  appearance: none;
  border-radius: 100%;
  margin-left: 0;
  margin-right: 0.25rem;
  background-color: white;
  border: 1px solid $midgrey;
}

input[type='radio']:checked {
  appearance: none;
  border-radius: 100%;
  margin-left: 0;
  margin-right: 0.25rem;
  background-color: $darkgrey;
  border: 3px solid $midgrey;
}

input[type='radio']:focus {
  outline: none;
}
</style>
