<template>
  <div class="qna">
    <div>
      <span>{{ title }}</span>
      <a v-if="!isMypage" href="#" @click.prevent="openQnARegister">등록하기</a>
      <div v-else>
        <label><input type="radio" name="answerType" checked>&nbsp;전체</label>
        <label><input type="radio" name="answerType">&nbsp;답변</label>
        <label><input type="radio" name="answerType">&nbsp;미답변</label>
      </div>
    </div>
    <QnARegister v-if="showQnA"></QnARegister>
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
        <template v-for="answer in answers">
          <tr @click.prevent="togleAnswer(answer)" :key="answer">
            <td v-if="!isMypage">배송 문의</td>
            <td><span>답변대기</span></td>
            <td><p class="scret">{{answer.title}}</p></td>
            <td>{{answer.register}}</td>
            <td>{{answer.regDate}}</td>
          </tr>
          <tr class="answer" v-show="answer.answerShow" :key="answer">
            <td v-if="!isMypage"></td>
            <td></td>
            <td><p class="scret">비밀글입니다.</p></td>
            <td></td>
            <td></td>
          </tr>
        </template>
        <!--
        <tr>
          <td>배송 문의</td>
          <td><span>답변대기</span></td>
          <td><p>비밀글입니다.</p></td>
          <td>dsd***</td>
          <td>2021.03.11</td>
        </tr> -->
      </tbody>
    </table>
    <Pagenation></Pagenation>
  </div>
</template>

<script>
// import { SERVER_IP } from '@/config.js'
// import axios from 'axios'
// import { VueAgile } from 'vue-agile'
// import mockup from '@/Data/DetailOption.json'
import Pagenation from '@/service/Components/Pagenation'
import QnARegister from '@/service/Detail/QnARegister'

export default {
  created () {
  },
  props: {
    title: String,
    isMypage: Boolean
  },
  data () {
    return {
      answers: [
        {
          title: '비밀글입니다.',
          regDate: '2021.03.11',
          regster: 'dsd***',
          answerShow: false
        },
        {
          title: '비밀글입니다.',
          regDate: '2021.03.11',
          regster: 'dsd***',
          answerShow: false
        }
      ],
      showQnA: false
    }
  },
  components: {
    Pagenation,
    QnARegister
  },
  methods: {
    togleAnswer (answer) {
      answer.answerShow = !answer.answerShow
    },
    openQnARegister () {
      // eslint-disable-next-line no-return-assign
      return this.showQnA = !this.showQnA
    }
  }
}
</script>

<style lang="scss" scoped>
.qna {
  display: flex;
  flex-wrap: wrap;

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
}
</style>
