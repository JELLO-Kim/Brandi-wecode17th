<template>
  <div>
    <a-descriptions bordered size="small" class="seller-from" label-width="20%">
      <a-descriptions-item :span="3">
        <template slot="label">판매가 <span class="required">*</span></template>
        <a-input placeholder="판매가" class="normal-size" suffix="원" v-model="data.salePrice" v-currency /><br/>
        <info-text label=" 판매가는 원화기준 10원 이상이며 가격 입력 시 10원 단위로 입력해 주세요."/>
      </a-descriptions-item>
      <a-descriptions-item label="할인정보" :span="3">
        <table class="bordered" style="width: 500px">
          <thead>
            <tr>
              <th width="130">할인율</th>
              <th>할인가</th>
            </tr>
          </thead>
          <tbody>
          <tr>
            <td><a-input suffix="%" v-mask="'###'" :min="0" :max="99" v-model.number="num" class="small-size" @blur="() => { if (num > 99) num = 99 } " /></td>
            <td>0 원 <a-button type="primary">할인판매가적용</a-button></td>
          </tr>
          <tr>
            <td>할인팬매가</td>
            <td>0 원</td>
          </tr>
          <tr>
            <td>할인기간</td>
            <td>
              <a-radio-group v-model="saleType">
                <a-radio :value="1">무기한</a-radio>
                <a-radio :value="2">기간설정</a-radio>
              </a-radio-group>
              <div v-show="saleType == 2">
                <a-range-picker class="range"/>
                <info-text label="할인기간을 설정시 기간만료되면 자동으로 정상가로 변경 됩니다."/>
              </div>
            </td>
          </tr>
          </tbody>
        </table>

        <info-text label="할인판매가 = 판매가 * 할인율"/><br/>
        <info-text label="할인 판매가 적용 버튼을 클릭 하시면 판매가 정보가 자동 계산되어집니다."/><br/>
        <info-text label="할인 판매가는 원화기준 10원 단위로 자동 반올림됩니다."/>

      </a-descriptions-item>
      <a-descriptions-item :span="3" label="최소/최대판매수량">
        <a-slider id="test" range :default-value="[1, 20]" :disabled="disabled" :min="1" :max="20" style="width: 250px" />
        <info-text label="최소/최대 판매수량은 1~20개 까지 지정 할 수 있습니다"/>
      </a-descriptions-item>
    </a-descriptions>
  </div>
</template>

<script>
// import ImageUpload from '@/admin/Components/Common/image-upload'
import InfoText from '@/admin/Components/Common/info-text'
export default {
  components: {
    InfoText
    // ImageUpload
  },
  data () {
    return {
      num: 0,
      value: 1000,
      sellerType: 1,
      saleType: 1,
      managers: [
        {
          name: '',
          email: '',
          phone_number: ''
        }
      ],
      data: {
        minSaleType: 1,
        maxSaleType: 1,
        minSaleCount: 0,
        salePrice: 0
      }
    }
  },
  methods: {
    addManager () {
      if (this.managers.length < 3) {
        this.managers.push({
          name: '',
          email: '',
          phone_number: ''
        })
      }
    },
    popManager () {
      if (this.managers.length > 1) this.managers.pop()
    }
  }
}
</script>

<style type="scss" scoped>
br + .normal-size {
  margin-top: 5px;
}
.required {
  color: red;
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
.range {
  margin: 5px 0;
}
hr {
  border: none;
  border-top: 1px solid #ccc;
}
table.bordered th {
  background: #fafafa;
}
table.bordered th,
table.bordered td {
  border: 1px solid #e8e8e8;
  padding: 10px 15px;
  font-size: 13px;
}
</style>
