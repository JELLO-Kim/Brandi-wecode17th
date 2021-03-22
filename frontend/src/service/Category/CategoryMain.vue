<template>
  <div class="container">
    <CategoryBreadCrumb class="bread-crumb"></CategoryBreadCrumb>
    <div class="left-menu">
      <ProductOption></ProductOption>
      <CategoryMenu class="category-menu"></CategoryMenu>
    </div>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import CategoryMenu from './CategoryMenu'
import ProductOption from './ProductOption'
import CategoryBreadCrumb from './CategoryBreadCrumb'

export default {
  name: 'CategoryMain',
  components: {
    CategoryMenu,
    ProductOption,
    CategoryBreadCrumb
  },
  data () {
    return {
      testCheck: false
    }
  }
}
</script>

<style lang="scss" scoped>
.container {
  display: flex;
  flex-wrap: wrap;

  .bread-crumb {
    width: 100%;
    height: 70px;
  }
  .left-menu {
    width: 212px;
    .category-menu {
      margin-top: 30px;
    }
  }
  .content {
    flex-grow: 1;
    width: 100px;
    margin-left: 20px;
    // background: #f1f1f1;
  }
}
</style>
