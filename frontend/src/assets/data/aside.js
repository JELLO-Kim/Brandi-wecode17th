export default [
  { name: '홈', param: 'home', url: 'admin/sellerdashboard' },
  {
    name: '주문관리',
    param: 'order',
    sub: [
      { name: '상품준비관리', param: 'prepare', url: 'admin/orders/readyproduct' },
      { name: '배송중관리', param: 'delivery', url: 'admin/orders/deliverproduct' },
      { name: '배송완료관리', param: 'deliverycomplete', url: 'admin/orders/arriveproduct' }
    ]
  },
  {
    name: '상품관리',
    param: 'product',
    sub: [
      { name: '상품 관리', param: 'manage', url: 'admin/products' },
      { name: '상품 등록', param: 'regist', url: 'admin/products/registerproduct' }
    ]
  },
  {
    name: '회원관리',
    param: 'account',
    sub: [
      { name: '셀러계정관리', param: 'seller', url: 'admin/sellers' }
    ]
  }
]
