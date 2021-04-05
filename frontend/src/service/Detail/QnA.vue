<template>
  <div class="qna">
    <div>
      <span>{{ title }}</span>
      <a v-if="!isMypage" href="#" @click.prevent="openQnARegister">등록하기</a>
      <div v-else>
        <label><input type="radio" v-model="answerType" value="" checked>&nbsp;전체</label>
        <label><input type="radio" v-model="answerType" value="1">&nbsp;답변</label>
        <label><input type="radio" v-model="answerType" value="0">&nbsp;미답변</label>
      </div>
    </div>
    <QnARegister v-bind:id="this.id" v-if="showQnA"></QnARegister>
    <table>
      <colgroup>
        <col v-if="!isMypage" width="15%">
        <col width="15%">
        <col>
        <col width="15%">
        <col width="15%">
      </colgroup>
      <thead>
        <tr>
          <th v-if="!isMypage">분류</th>
          <th v-if="!isMypage">처리상태</th>
          <th v-if="isMypage">답변상태</th>
          <th>내용</th>
          <th>작성자</th>
          <th>작성일</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="answer in qnaList">
          <tr @click.prevent="togleAnswer(answer)" :key="answer">
            <td v-if="!isMypage">배송 문의</td>
            <td><span>{{ answer.isFinished == 1 ? '답변완료' : '답변대기'}}</span></td>
            <td><p class="scret">{{answer.contents}}</p></td>
            <td><p v-if="!isMypage">{{answer.writer}}</p></td>
            <td>{{answer.createdAt}}</td>
          </tr>
          <tr class="answer" :class="QnA.answer.isShow" v-if="QnA.answer" :key="answer.answer">
            <td v-if="!isMypage"></td>
            <td></td>
            <td><p class="scret" v-if="answer.answer">{{answer.answer.contents}}.</p></td>
            <td><p v-if="answer.answer">{{answer.answer.replier}}.</p></td>
            <td><p v-if="answer.answer">{{answer.answer.createdAt}}</p></td>
          </tr>
        </template>
      </tbody>
    </table>
    <div class="pagination">
      <a-pagination
        v-model="current"
        :page-size.sync="pageSize"
        :total="qnaTotal"
        @change="changePage"
      ></a-pagination>
    </div>
  </div>
</template>

<script>
// import axios from 'axios'
// import { VueAgile } from 'vue-agile'
// import mockup from '@/Data/DetailOption.json'
// import Pagenation from '@/service/Components/Pagenation'
import QnARegister from '@/service/Detail/QnARegister'
// eslint-disable-next-line no-unused-vars
import SERVER from '@/config'
// eslint-disable-next-line no-unused-vars
import API from '@/service/util/service-api'

export default {
  created () {
    this.loadData()
  },
  props: {
    title: String,
    isMypage: Boolean // 마이페이지 여부 (false => 상품)
  },
  data () {
    return {
      qnaList: [],
      qnaTotal: 0,
      showQnA: false,
      pageSize: 5,
      current: 1,
      answerType: '' // 0: 미답변, 1: 답변 없으면 전체
    }
  },
  components: {
    // Pagenation,
    QnARegister
  },
  methods: {
    changePage () {
      this.loadData()
    },
    loadData () {
      const params = {
        limit: this.pageSize,
        offset: this.pageSize * (this.current - 1)
      }
      if (this.answerType) {
        params.answer = this.answerType
      }
      const url = this.isMypage ? `${SERVER.IP}/mypage/qna` : `${SERVER.IP}/products/${this.$route.params.id}/question`
      API.methods
        .get(url, {
          params: params
        })
        .then((res) => {
          this.qnaList = res.data.result.data
          this.qnaTotal = res.data.result.totalCount
        })
        .catch(() => {
          // console.log(error)
          this.$router.push('/main')
          alert('존재하지 않는 서비스 상품입니다.')
        })
    },
    togleAnswer (answer) {
      this.$set(answer, 'answerShow', !answer.answerShow)
      // answer.answerShow = !answer.answerShow
    },
    openQnARegister () {
      // eslint-disable-next-line no-return-assign
      return this.showQnA = !this.showQnA
    }
  },
  watch: {
    answerType () {
      this.loadData()
    }
  }
}
</script>

<style lang="scss" scoped>
.qna {
  display: flex;
  flex-wrap: wrap;

  .pagination {
    margin: 20px;
  }

  div:first-child {
    display: flex;
    width: 100%;
    justify-content: space-between;
    font-size: 2em;
    color: black;
    padding-bottom: 10px;

    span {
      font-weight: 600;
    }
    a {
      color: #000;
    }

    label {
      margin-left: 15px;
      input {
          width: 15px;
          height: 15px;
      }
    }
  }

  table {
    width: 100%;
    border-collapse: 0;
    border-top: 1px solid #000;
    font-size: 18px;
    thead {
      border-bottom: 1px solid #CCC;
      text-align: center;
      th {
        height: 60px;
      }
    }
    tbody {
      tr {
        border-bottom: 1px solid #F1F1F1;
        td {
          text-align: center;
          height: 50px;
          color: #000;
          span {
            display: inline-block;
            border: 1px solid #CCC;
            font-size: 14px;
            color: #999;
            padding: 3px 13px;
            border-radius: 15px;
          }
          p {
            margin: 0;
            text-align: left;
          }
        }
        &.answer td {
          background: #F6F6F6;
          color: #999;
        }
      }
    }
  }

  .pagination {
    margin-top: 30px;
  }
}
</style>
