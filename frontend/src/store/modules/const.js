export default {
  namespaced: true,
  state: {
    sellerSections: [
      { label: '쇼핑몰', value: 1 },
      { label: '마켓', value: 2 },
      { label: '로드샵', value: 3 },

      { label: '디자이너브랜드', value: 4 },
      { label: '제너럴브랜드', value: 5 },
      { label: '내셔널브랜드', value: 6 },

      { label: '뷰티', value: 7 }
    ],
    saleTypes: [
      { label: '판매', value: 1 },
      { label: '미판매', value: 0 }
    ],
    sellerStatus: [
      { label: '입점대기', value: 1 },
      { label: '입점', value: 2 },
      { label: '휴점', value: 3 },
      { label: '퇴점대기', value: 4 },
      { label: '퇴점', value: 5 },
      { label: '입점거절', value: 6 }
    ],
    // button - 입점거절:1 입점승인:2 휴점처리:3 휴점해제:4 퇴점대기:5 퇴점철회:6 퇴점확정:7
    sellerStatusActions: {
      1: [
        { label: '입점승인', value: 2, type: 'info' },
        { label: '입점거절', value: 1, type: 'danger' }
      ],
      2: [
        { label: '휴점처리', value: 3, type: 'warning' },
        { label: '퇴점신청', value: 5, type: 'danger' }
      ],
      3: [
        { label: '휴점해제', value: 4, type: 'success' },
        { label: '퇴점신청', value: 5, type: 'danger' }
      ],
      4: [
        { label: '퇴점해제', value: 6, type: 'info' },
        { label: '퇴점승인', value: 7, type: 'danger' }
      ]
    },
    exhibitTypes: [
      { label: '진열', value: 1 },
      { label: '미진열', value: 0 }
    ],
    discountTypes: [
      { label: '할인', value: 1 },
      { label: '미할인', value: 0 }
    ],
    orderStatusTypes: [
      { label: '상품 준비 관리', value: 1 },
      { label: '배송중 관리', value: 2 },
      { label: '배송완료 관리', value: 3 },
      { label: '구매확정 관리', value: 4 }
    ],
    colors: ['Black', 'White', 'Gray', 'Ivory', 'Navy', 'Brown', 'Wine', 'Purple', 'Green', 'Blue', 'Red', 'Pink', 'Khaki', 'Yellow', 'Beige', 'Light Pink', 'Light Blue', 'Light Green', 'Peach', 'Silver', 'Gold', 'Orange', '유광', '무광', 'Violet', 'Middle Blue', 'Mint', 'Deep Blue', 'Lime', 'Mustard', 'Light Purple', 'IndiPink', 'Camel', 'Charcoal', 'Sky Blue', 'Deep Pink', 'Dark Blue', 'Rose Gold', 'Dark Brown', 'Light Brown', 'Light Gray', 'Dark Gray', 'Brick Red', 'Olive', 'Burgundy', 'Dark Green', 'Cocoa', 'Oatmeal', 'Light Beige', 'Bluegreen', 'Marsala', 'Cream', 'Mocha', 'DeepGreen', 'Lavender', 'LightKhaki', 'Lemon', 'RoseBrown', 'DarkBeige', 'Stripe', 'Check', 'Melange', 'Denim', 'VioletPink', 'KhakiGray', 'Taupe', 'Deepbeige', 'Melangegray', '고방체크', '글랜체크', 'Stripe Red', 'flower', 'Dot', 'Lilac', 'Cappuccino', 'Bright green', 'Hot pink', 'Blue Denim', 'Leopard', '블랙', '화이트', '그레이', '아이보리', '네이비', '블루', '레드', '핑크', '옐로우', '베이지', '연청', '민트', '진청', '연베이지', '중청', '소라', '그린', '연퍼플', '머스터트', '퍼플', '청록', 'COMOUFLAGE', 'ETHNIC-WHITE', '연핑크', '딥핑크', '인디핑크', '딥그린', '카키', '와인', '브라운', '실버', '크림', '차콜', '오렌지', 'BBB', 'BLUEJEAN', 'CARGO', 'GWR', 'INCA', 'IQUASSU', 'MAYA', 'NON', 'NWN', 'NWR', 'NWRWN', 'NYN', 'YRB', 'BLACK STRIPE', 'RED STRIPE', 'BLACK DOT', 'NAVY DOT', 'BK D+NA D', 'BK S+RED S', 'NWR+BLACK', 'BLACK+BLACK', 'NWR+NWN', 'BEIGE+GREY', 'NWN+NWN', 'BK D+BLACK', 'NWR+NWR', 'CARGO+BEIGE', 'GREY+GREY', 'BK D+BK D', 'BK S+BK S', '올리브', '라이트베이지', '다크베이지', '골드', '라임', '라이트블루', 'pinkbeige', '그레이/끈탱크탑(탱크탑)', '그레이/숏탱크탑(미니브라탑)', '그레이/탱크탑(기본탱크탑)', '그레이/튜브탑(튜브탑)', '베이지/끈탱크탑(탱크탑)', '베이지/숏탱크탑(미니브라탑)', '베이지/탱크탑(기본탱크탑)', '베이지/튜브탑(튜브탑)', '블랙(착샷)/숏탱크탑(미니브라탑)', '블랙(착샷)/튜브탑(튜브탑)', '블랙/끈탱크탑(탱크탑)', '블랙/탱크탑(기본탱크탑)', '아이보리/끈탱크탑(탱크탑)', '아이보리/숏탱크탑(미니브라탑)', '아이보리/탱크탑(기본탱크탑)', '아이보리/튜브탑(튜브탑)', '피치핑크', '오트밀', 'bokashi gray', 'navy/stripe'],
    sizes: ['Free', 'XL', 'L', 'M', 'S', 'XS', '25', '26', '27', '28', '29', '225', '230', '235', '240', '245', '250', '255', '30', '32', '34', '36', '1호', '2호', '3호', '4호', '5호', '6호', '7호', '8호', '9호', '10호', '11호', '12호', '13호', '14호', '15호', '16호', '17호', '18호', '19호', '37[235~240]', '38[240~245]', '39[245~250]', '40[255~260]', '41[260~265]', '42[270~275]', '43[275~280]', '44[280~285]', '45[285~290]', '34[220~225]', '35[225~230]', '36[230~235]', '220', '260', '270', '280', '35', '37', '38', '39', '40', '210', '215', '265', '275', '285', '290', '85', '90', '95', '100', '105', '70a', '70b', '70c', '70d', '70e', '70f', '70g', '75a', '75b', '75c', '75d', '75e', '75f', '75g', '75ab', '75bc', '80a', '80b', '80c', '80d', '80e', '80f', '80g', '80ab', '80bc', '85a', '85b', '85c', '85d', '85e', '85f', '85g', '90a', '90b', '90c', '90d', '90e', '90f', '90g', '95a', '95b', '95c', '95d', '95e', '95f', '95g', '100a', '100b', '100c', '100d', '100e', '100f', '100g', '105a', '105b', '105c', '105d', '105e', '105f', '105g', '아이폰5s/SE', '아이폰6/6S', '아이폰6플러스/6s플러스', '아이폰7', '아이폰7플러스', '갤럭시S7', '갤럭시S7엣지', '갤럭시S8', '갤럭시S8플러스', '갤럭시노트5', '아이폰6s플러스/7플러스', '13인치', '15인치', '85ab', '70ab', 'A컵', 'B컵', 'C컵', 'D컵', 'XXL', 'XXXL', 'XXXXL', 'M(44-55)', 'L(55-66)', 'L(55-마른66)', '아이폰8', '아이폰8플러스', '아이폰X', '갤럭시S9', '갤럭시S9플러스', '갤럭시노트7', '갤럭시노트8'],
    firstCategory: [{ text: '아우터', value: '3' }, { text: '상의', value: '2' }, { text: '바지', value: '50' }, { text: '원피스', value: '33' }, { text: '스커트', value: '47' }, { text: '신발', value: '5' }, { text: '가방', value: '6' }, { text: '주얼리', value: '119' }, { text: '잡화', value: '10' }, { text: '라이프웨어', value: '107' }, { text: '빅사이즈', value: '362' }],
    secondCategory: [{ text: '자켓', value: '20' }, { text: '가디건', value: '18' }, { text: '코트', value: '21' }, { text: '점퍼', value: '22' }, { text: '패딩', value: '493' }, { text: '무스탕/퍼', value: '494' }, { text: '기타', value: '495' }],
    orderDateFilter: [{ label: '오늘', value: 1 }, { label: '3일', value: 3 }, { label: '1주', value: 7 }, { label: '1개월', value: 30 }, { label: '3개월', value: 90 }],
    orderCodeMask: {
      mask: 'CCCCCCCCCCCCCCCCC',
      tokens: {
        C: {
          pattern: /[a-zA-Z0-9]/, transform: v => v.toLocaleUpperCase()
        }
      }
    },
    apiDomain: 'http://192.168.40.105:5000',
    testToken: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZWxsZXJfaWQiOjQsImV4cCI6MTYwNDY1NzU1N30.i4HTrIJWfnQ_tjf4D2WyziEK5j6KOK_GGhenbMfdTH8'
  },
  getters: {
  },
  mutations: {
  },
  actions: { /* 통신처리 */
  }
}
