<template>
  <div>
    <h2>
      Q&A (192)
      <a href="#">문의하기</a>
    </h2>
    <table>
      <colgroup>
        <col width="15%">
        <col width="15%">
        <col>
        <col width="15%">
        <col width="15%">
      </colgroup>
      <thead>
        <tr>
          <th>분류</th>
          <th>처리상태</th>
          <th>내용</th>
          <th>작성자</th>
          <th>작성일</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="answer in answers">
          <tr @click.prevent="togleAnswer(answer)" :key="answer">
            <td>배송 문의</td>
            <td><span>답변대기</span></td>
            <td><p class="scret">{{answer.title}}</p></td>
            <td>{{answer.register}}</td>
            <td>{{answer.regDate}}</td>
          </tr>
          <tr class="answer" v-show="answer.answerShow" :key="answer">
            <td></td>
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

export default {
  created () {
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
      ]
    }
  },
  components: {
    Pagenation
  },
  methods: {
    togleAnswer (answer) {
      answer.answerShow = !answer.answerShow
    }
  }
}
</script>

<style lang="scss" scoped>
h2 {
  display: flex;
  justify-content: space-between;
  a {
    color: #000;
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
</style>
