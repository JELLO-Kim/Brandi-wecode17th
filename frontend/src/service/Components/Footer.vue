<template>
  <footer class="mainFooter">
    <div class="footerTop">
      <div class="customerService">
        <div class="phoneNumber">고객센터 1566-6575</div>
        <div class="businessHour">영업시간 : AM 10:00 ~ PM 17:00 (주말 및 공휴일 휴무)</div>
        <div class="businessHour">점심시간 : PM 12:30 ~ PM 13:30</div>
      </div>
      <div class="snsLink">
        <div class="snsContainer">
          <div class="imgContainer">
            <img src="/images/icon_footer_01.png" alt="FAQ" />
          </div>
          <div>자주 묻는 질문</div>
        </div>
        <div class="snsContainer">
          <div class="imgContainer">
            <img src="/images/icon_footer_02.png" alt="kakaoTalk" />
          </div>
          <div>카톡 플러스 친구</div>
        </div>
        <div class="snsContainer">
          <div class="imgContainer">
            <img src="/images/icon_footer_03.png" alt="faceBook" />
          </div>
          <div>페이스북</div>
        </div>
        <div class="snsContainer">
          <div class="imgContainer">
            <img src="/images/icon_footer_04.png" alt="instagram" />
          </div>
          <div>인스타그램</div>
        </div>
      </div>
    </div>
    <div class="footerBottom">
      <div class="bottomLeft">
        <div class="companyInfo">
          회사명 : (주)브랜디 | 대표이사 : 서정민 | 사업자등록번호 :
          220-88-93187 | 통신판매업신고 : 2016-서울강남-00359 | 호스팅사업자 :
          (주)브랜디
        </div>
        <div class="companyInfo">주소 : (06223) 서울특별시 강남구 테헤란로 32길 26 청송빌딩</div>
        <div class="companyInfo">개인정보관리책임자 : 윤석호(privacy@brandi.co.kr)</div>
        <div class="companyInfo">
          브랜디는 통신판매중개자로서 통신판매 당사자가 아니며, 판매자가 등록한
          상품정보 및 거래에 브랜디는 책임을 지지 않습니다.
        </div>
        <div class="terms">
          <a href="#" class="link">이용약관</a>
          <div class="divider"></div>
          <a href="#" class="link" id="linkCenter">개인정보처리방침</a>
          <div class="divider"></div>
          <a href="#" class="link">사업자정보확인</a>
        </div>
      </div>
      <div class="snsLink">
        <div class="snsContainer" id="linkToAdmin" @click="linkToAdmin">
          <div class="imgContainer">
            <img src="/images/icon_footer_05.png" alt="sellerAdmin" />
          </div>
          <div>셀러어드민</div>
        </div>
        <div class="snsContainer">
          <div class="imgContainer">
            <img src="/images/icon_footer_06.png" alt="sellerIn" />
          </div>
          <div>입점문의</div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  methods: {
    linkToAdmin () {
      this.$router.push('/admin')
    }
  }
}
</script>

<style lang="scss" scoped>
#linkToAdmin {
  cursor: pointer;
}
.mainFooter {
  background-color: black;
  position: relative;

  .footerTop {
    border-bottom: 0.5px solid rgba(128, 128, 128, 0.5);
    display: flex;
    justify-content: space-between;
    max-width: 1250px;
    margin-left: auto;
    margin-right: auto;
    padding: 30px 0 35px 0;

    .phoneNumber {
      color: white;
      font-size: 33px;
      font-weight: bold;
      margin-bottom: 20px;
    }

    .businessHour {
      color: gray;
      font-size: 14px;
      margin-bottom: 5px;
    }
  }

  .footerBottom {
    display: flex;
    justify-content: space-between;
    max-width: 1250px;
    margin-left: auto;
    margin-right: auto;
    padding: 40px 0 60px 0;

    .bottomLeft {
      .companyInfo {
        color: gray;
        font-size: 14px;
        padding-bottom: 5px;
      }

      .terms {
        display: flex;
        margin-top: 10px;

        .divider {
          background-color: white;
          width: 0.5px;
          margin: 0 10px;
        }

        #linkCenter {
          font-weight: bold;
        }
      }
    }
  }
  .snsLink {
    color: white;
    font-size: 14px;
    display: flex;
    margin-bottom: 70px;

    .snsContainer {
      display: flex;
      align-items: center;
      padding-right: 5px;

      .imgContainer {
        img {
          width: 30px;
          margin-left: 10px;
          margin-right: 3px;
        }
      }
    }
  }

  .link {
    font-size: 14px;
    text-decoration: none;
    color: white;
  }
}
</style>
