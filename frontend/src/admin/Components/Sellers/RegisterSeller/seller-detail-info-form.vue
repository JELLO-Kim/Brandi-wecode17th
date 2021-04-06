<template>
  <div>
    <a-descriptions bordered size="small" class="seller-from" label-width="20%">
      <a-descriptions-item label="셀러페이지 배경이미지" :span="3">
        <image-upload  v-model="dataStore.detailData.backgroundImage" />
      </a-descriptions-item>
      <a-descriptions-item :span="3">
        <template slot="label">셀러 한줄 소개 <span class="required">*</span></template>
        <a-input placeholder="셀러 한줄 소개" class="normal-size" v-model="dataStore.detailData.introduce"/>
      </a-descriptions-item>
      <a-descriptions-item label="셀러 상세 소개" :span="3">
        <a-textarea placeholder="셀러 상세 소개" v-model="dataStore.detailData.description"></a-textarea>
      </a-descriptions-item>
<!--      <a-descriptions-item :span="3">-->
<!--        <template slot="label">사이트 URL <span class="required">*</span></template>-->
<!--        <a-input placeholder="셀러 한줄 소개" class="normal-size" v-model="dataStore.detailData.detail_introduce"/>-->
<!--      </a-descriptions-item>-->
          {{dataStore.detailData.managers}}
      <a-descriptions-item :span="3">
        <template slot="label">담당자 정보 <span class="required">*</span></template>
        <div v-for="(item, i) in dataStore.detailData.managers" :key="i">
          <hr v-if="i > 0">
          <div class="manager">
            <a-input placeholder="담당자명" class="normal-size" v-model="item.name" /><br/>
            <a-input placeholder="담당자 핸드폰번호" class="normal-size" v-model="item.phoneNumber" v-mask="'###-####-####'" /><br/>
            <a-input placeholder="담당자 이메일" class="normal-size" v-model="item.email"/>
          </div>
          <div v-show="dataStore.detailData.managers.length-1 == i" class="manager-button">
            <a-button type="success" @click="addManager" v-show="dataStore.detailData.managers.length < 3">+</a-button>
            <a-button type="danger" @click="popManager" v-show="dataStore.detailData.managers.length > 1">-</a-button>
          </div>
        </div>
      </a-descriptions-item>
<!--      <a-descriptions-item :span="3">-->
<!--        <template slot="label">인스타그램 아이디 <span class="required">*</span></template>-->
<!--        <a-input placeholder="인스타그램 아이디" class="normal-size" />-->
<!--      </a-descriptions-item>-->
      <a-descriptions-item :span="3">
        <template slot="label">고객센터 <span class="required">*</span></template>
        <a-input placeholder="고객센터 전화번호" class="normal-size" v-model="dataStore.detailData.customerServicePhone"  v-mask="'###-####-####'" /><br/>
        <a-input placeholder="고객센터명" class="normal-size" v-model="dataStore.detailData.customerServiceName" /><br/>
<!--        <a-input placeholder="카카오톡 아이디" class="normal-size" /><br/>-->
<!--        <a-input placeholder="옐로우 아이디" class="normal-size" />-->
      </a-descriptions-item>
<!--      <a-descriptions-item :span="3">-->
<!--        <template slot="label">택배주소 <span class="required">*</span></template>-->
<!--        <a-input placeholder="고객센터 전화번호" class="normal-size" />-->
<!--        <a-button type="success" class="find-post-button">우편번호 찾기</a-button><br/>-->
<!--        <a-input placeholder="카카오톡 아이디" class="normal-size" /><br/>-->
<!--        <a-input placeholder="상세주소 (택배수령지)" class="normal-size" />-->
<!--      </a-descriptions-item>-->
      <a-descriptions-item :span="3">
        <template slot="label">고객센터 운영시간 (주중) <span class="required">*</span></template>
        <a-input v-model="dataStore.detailData.customerServiceOpen" maxlength="2" placeholder="영업시작시간" />
        ~ <a-input v-model="dataStore.detailData.customerServiceClose" maxlength="2" placeholder="영업종료시간" />
        <a-input v-model="dataStore.detailData.postal" placeholder="우편번호" />
        <a-input v-model="dataStore.detailData.address" placeholder="주소" />
        <a-input v-model="dataStore.detailData.addressDetail" placeholder="상세주소" />
      </a-descriptions-item>
<!--      <a-descriptions-item :span="3">-->
<!--        <template slot="label">정산정보 입력 <span class="required">*</span></template>-->
<!--        <a-input placeholder="고객센터 전화번호" class="normal-size" /><br/>-->
<!--        <a-input placeholder="계좌번호" class="normal-size" /><br/>-->
<!--        <a-input placeholder="계좌주" class="normal-size" />-->
<!--      </a-descriptions-item>-->
      <a-descriptions-item :span="3" label="샐러상태 변경이력">

        <table class="bordered">
          <thead>
          <tr>
            <th>셀러상태 변경 적용일시</th>
            <th>셀러 상태</th>
            <th>변경 실행자</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="item in dataStore.detailData.status_histories" :key="item">
            <td>{{ item.update_time }}</td>
            <td>{{ getSellerStatusName(item.seller_status_id) }}</td>
            <td>{{ item.account }}</td>
          </tr>
          </tbody>
        </table>
      </a-descriptions-item>

    </a-descriptions>
  </div>
</template>

<script>
import CommonMixin from '@/admin/mixins/common-mixin'
import ImageUpload from '@/admin/Components/Common/image-upload'
export default {
  components: {
    ImageUpload
  },
  mixins: {
    CommonMixin
  },
  data () {
    return {
      sellerType: 1
    }
  },
  props: {
    dataStore: {
      default () {
        return {
          detailData: {
            managers: []
          }
        }
      }
    }
  },
  computed: {
    constants () {
      return this.$store.state.const
    }
  },
  methods: {
    addManager () {
      if (this.dataStore.detailData.managers.length < 3) {
        // backupDetailData
        let id = null
        if (this.dataStore.backupDetailData.managers.length > this.dataStore.detailData.managers.length) {
          id = this.dataStore.backupDetailData.managers[this.dataStore.detailData.managers.length].id
        }
        this.dataStore.detailData.managers.push({
          id: id,
          name: '',
          email: '',
          phone_number: ''
        })
      }
    },
    popManager () {
      if (this.dataStore.detailData.managers.length > 1) { this.dataStore.detailData.managers.pop() }
    },
    getSellerStatusName (statusId) {
      const statusItem = this.constants.sellerStatus.filter((d) => { return d.value === statusId })
      if (statusItem.length > 0) return statusItem[0].label
      return ''
    }
  }
}
</script>

<style type="scss" scoped>
.normal-size {
  width: 200px;
}
br + .normal-size {
  margin-top: 5px;
}
.required {
  color: red
}
.manager {
  display: inline-block;
}
.manager-button {
  display: inline-block;
}
.find-post-button {
  margin-left: 5px;
}
hr {
  border: none;
  border-top: 1px solid #CCC;
}
table.bordered th {
  background: #fafafa;
}
table.bordered th, table.bordered td{
  border: 1px solid #e8e8e8;
  padding: 10px 15px;
  font-size: 13px;
}

</style>
