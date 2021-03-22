import Vue from 'vue'
import Router from 'vue-router'

import Main from '@/service/Main/Main'
import Layout from '@/service/Layout'
import Detail from '@/service/Detail/Detail'
import Login from '@/service/Login/Login'
import SignUp from '@/service/SignUp/SignUp'
import CategoryMain from '@/service/Category/CategoryMain'
// import VueAgile from "vue-agile";
// import AdminFrame from "../BrandiAdmin/Components/AdminFrame.vue";
// import ProductRegistration from "../BrandiAdmin/ProductRegistration/ProductRegistration.vue";
import Order from '@/service/Order/Order'
import Event from '@/service/Event/Event'
import EventDetail from '@/service/Event/EventDetail'
// import Footer from "@/service/Components/Footer.vue";
// import ProductManagement from "../BrandiAdmin/ProductManagemnet/ProductManagement.vue";
import Mypage from '@/service/Mypage/Mypage'
import OrderList from '@/service/Mypage/OrderList'
import Coupon from '@/service/Mypage/Coupon'
import Point from '@/service/Mypage/Point'
// import OrderManagement from "../BrandiAdmin/OrderManagement/OrderManagement.vue";
import OrderDetail from '@/service/OrderDetail/OrderDetail'
// import ProductDetail from "../BrandiAdmin/ProductDetail/ProductDetail.vue";
// import UserManagement from "../BrandiAdmin/UserManagement/UserManagement.vue";
import NetworkError from '@/service/Components/NetworkError'
import NotFound from '@/service/Components/NotFound'

import AdminLogin from '@/admin/Components/Login/Login'
import AdminSignUp from '@/admin/Components/SignUp/SignUp'

import Admin from '@/admin/Components/Admin'
import AdminSellerDashBoard from '@/admin/Components/SellerDashBoard/SellerDashBoard'

import AdminSellers from '@/admin/Components/Sellers/Sellers'
import AdminSellerList from '@/admin/Components/Sellers/SellerList/SellerList'
import AdminRegisterSeller from '@/admin/Components/Sellers/RegisterSeller/RegisterSeller'

import AdminProducts from '@/admin/Components/Products/Products'
import AdminProductList from '@/admin/Components/Products/ProductList/ProductList'
import AdminRegisterProduct from '@/admin/Components/Products/RegisterProduct/RegisterProduct'

import AdminOrders from '@/admin/Components/Orders/Orders'
import AdminOrderList from '@/admin/Components/Orders/OrderList/OrderList'
import AdminDetailOrder from '@/admin/Components/Orders/DetailOrder/DetailOrder'

// start
import Cart from '@/service/Cart/Cart'

Vue.use(Router)
export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: Layout,
      children: [
        {
          path: 'main',
          component: Main
        },
        {
          path: 'category',
          component: CategoryMain
        },
        {
          path: '/detail/:id',
          component: Detail
        },
        {
          path: '/login',
          component: Login
        },
        {
          path: '/signup',
          component: SignUp
        },
        {
          path: '/order',
          component: Order
        },
        {
          path: '/event',
          component: Event,
          name: 'event'
        },
        {
          path: '/event/:no',
          component: EventDetail,
          name: 'eventDetail'
        },
        {
          path: '/cart',
          component: Cart,
          name: 'cart'
        },
        {
          path: '/mypage',
          redirect: '/mypage/orderList',
          component: Mypage,
          name: Mypage,
          children: [
            {
              path: '',
              redirect: '/mypage/orderList',
              component: OrderList,
              name: 'orderList'
            },
            {
              path: 'orderList',
              component: OrderList,
              name: 'orderList'
            },
            {
              path: 'point',
              component: Point,
              name: 'point'
            },
            {
              path: 'coupon',
              component: Coupon,
              name: 'coupon'
            },
            {
              path: 'qna',
              component: Mypage,
              name: 'qna'
            },
            {
              path: 'faq',
              component: Mypage,
              name: 'faq'
            }
          ]
        },
        {
          path: '/order/detail',
          component: OrderDetail
        },
        {
          // 초기 url을 main으로 적용
          path: '/',
          redirect: '/main'
        },
        {
          path: '*',
          redirect: '/error/404'
        },
        {
          path: '/error/400',
          component: NetworkError
        },
        {
          path: '/error/404',
          component: NotFound
        }
      ]
    },
    // {
    //   path: '/main',
    //   component: Main
    // },
    // {
    //   path: '/detail/:id',
    //   component: Detail
    // },
    // {
    //   path: '/login',
    //   component: Login
    // },
    // {
    //   path: '/signup',
    //   component: SignUp
    // },
    // {
    //   path: '/order',
    //   component: Order
    // },
    // {
    //   path: '/event',
    //   component: Event,
    //   name: 'event'
    // },
    // {
    //   path: '/event/:no',
    //   component: EventDetail,
    //   name: 'eventDetail'
    // },
    // {
    //   path: '/mypage',
    //   redirect: '/mypage/orderList',
    //   component: Mypage,
    //   name: Mypage,
    //   children: [
    //     {
    //       path: '',
    //       redirect: '/mypage/orderList',
    //       component: OrderList,
    //       name: 'orderList'
    //     },
    //     {
    //       path: 'orderList',
    //       component: OrderList,
    //       name: 'orderList'
    //     },
    //     {
    //       path: 'point',
    //       component: Point,
    //       name: 'point'
    //     },
    //     {
    //       path: 'coupon',
    //       component: Coupon,
    //       name: 'coupon'
    //     },
    //     {
    //       path: 'qna',
    //       component: Mypage,
    //       name: 'qna'
    //     },
    //     {
    //       path: 'faq',
    //       component: Mypage,
    //       name: 'faq'
    //     }
    //   ]
    // },
    // {
    //   path: '/order/detail',
    //   component: OrderDetail
    // },
    // {
    //   // 초기 url을 main으로 적용
    //   path: '/',
    //   redirect: '/main'
    // },
    // {
    //   path: '*',
    //   redirect: '/error/404'
    // },
    // {
    //   path: '/error/400',
    //   component: NetworkError
    // },
    // {
    //   path: '/error/404',
    //   component: NotFound
    // },

    // 로그인
    {
      path: '/admin/login',
      name: 'Login',
      component: AdminLogin
    },

    // 회원가입
    {
      path: '/admin/signup',
      name: 'SignUp',
      component: AdminSignUp
    },

    // 어드민 내부
    {
      path: '/admin',
      name: 'Admin',
      component: Admin,

      children: [
        // 셀러 대쉬보드
        {
          path: 'sellerdashboard',
          name: 'SellerDashBoard',
          component: AdminSellerDashBoard
        },

        // 회원관리
        {
          path: 'sellers',
          name: 'Sellers',
          component: AdminSellers,

          children: [
            // 회원관리 > 셀러계정관리
            {
              path: '',
              name: 'SellerList',
              component: AdminSellerList
            },
            // 회원관리 > 회원등록
            {
              path: 'registerseller',
              name: 'RegisterSeller',
              component: AdminRegisterSeller
            },
            // 회원관리 > 회원수정
            {
              path: ':sellerNo',
              name: 'ModifySeller',
              component: AdminRegisterSeller,
              props: true
            }
          ]
        },

        // 상품관리
        {
          path: 'products',
          name: 'Products',
          component: AdminProducts,
          children: [
            // 상품관리 > 상품관리
            {
              path: '',
              name: 'ProductList',
              component: AdminProductList
            },
            // 상품관리 > 상품등록
            {
              path: 'registerproduct',
              name: 'RegisterProduct',
              component: AdminRegisterProduct
            },
            // 상품관리 > 상품수정
            {
              path: ':productNo',
              name: 'RegisterProduct',
              component: AdminRegisterProduct
            }
          ]
        },
        // 주문관리
        {
          path: 'orders',
          name: 'Orders',
          component: AdminOrders,
          children: [
            //  주문관리 > 상품준비 관리
            {
              path: 'readyproduct',
              name: 'Readyproduct',
              props: (route) => ({ status_id: 1 }),
              component: AdminOrderList
            },
            // 주문관리 > 배송중 관리
            {
              path: 'deliverproduct',
              name: 'DeliverProduct',
              props: (route) => ({ status_id: 2 }),
              component: AdminOrderList
            },
            // 주문관리 > 배송완료 관리
            {
              path: 'arriveproduct',
              name: 'ArriveProduct',
              props: (route) => ({ status_id: 3 }),
              component: AdminOrderList
            },
            // 주문관리 > 구매확정 관리
            {
              path: 'confirmProduct',
              name: 'ConfirmProduct',
              props: (route) => ({ status_id: 4 }),
              component: AdminOrderList
            },
            // 주문관리 > 주문 상세페이지
            {
              path: ':detailNo',
              name: 'Detail',
              component: AdminDetailOrder,
              props: true
            }
          ]
        }
      ]
    }
  ]
})
