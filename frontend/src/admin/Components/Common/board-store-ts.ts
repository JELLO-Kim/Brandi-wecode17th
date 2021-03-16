//
// class BoardStoreTs {
//   private name: string;
//   private total: number = 0;
//   private list: Array<Object> = [];
//   private page: number = 1;
//   private pageLen: number = 10;
//   private loading: boolean = false;
//   // loadUri: 'http:/aaaa.com/notice/list',
//
//   constructor(name: string) {
//     this.name = name;
//   }
//
//   load(): void {
//
//   }
//
// }

export const namespaced = true;

export interface ProductInfo {
  productNo: number,
  name: string
}

interface State {
  pageName: string,
  product: ProductInfo
}

export const state: State = {
  pageName: '상품 페이지',
  product: {
    productNo: 0,
    name: '상품 이름'
  }
}
