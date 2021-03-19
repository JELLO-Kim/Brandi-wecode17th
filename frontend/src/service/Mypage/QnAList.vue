<template>
    <div class="qna-list">
        <div>
            <div>
                <span>상품 Q&A</span>
            </div>
            <div>
                <span>
                    <label><input type="radio" name="qna-filter" checked>&nbsp;전체</label>
                    <label><input type="radio" name="qna-filter">&nbsp;답변</label>
                    <label><input type="radio" name="qna-filter">&nbsp;미답변</label>
                </span>
            </div>
        </div>
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
                    <th>답변상태</th>
                    <th>내용</th>
                    <th>작성자</th>
                    <th>작성일</th>
                </tr>
            </thead>
            <tbody>
                <template v-for="answer in answers">
                <tr @click.prevent="togleAnswer(answer)" :key="answer">
                    <td>배송 문의</td>
                    <td><p class="scret">{{answer.title}}</p></td>
                    <td>{{answer.register}}</td>
                    <td>{{answer.regDate}}</td>
                </tr>
                <tr class="answer" v-show="answer.answerShow" :key="answer">
                    <td></td>
                    <td><p class="scret">비밀글입니다.</p></td>
                    <td></td>
                    <td></td>
                </tr>
                </template>
            </tbody>
        </table>
        <!-- <Pagenation></Pagenation> -->
    </div>
</template>

<script>
// import Pagenation from '@/service/Components/Pagenation'

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
    // Pagenation
  },
  methods: {
    togleAnswer (answer) {
      answer.answerShow = !answer.answerShow
    }
  }
}
</script>

<style lang="scss" scoped>
.qna-list {
    display: flex;
    flex-direction: column;
    padding: 20px;
    color: #1e1e1e;

    div {
        display: flex;
        justify-content: space-between;
        font-size: 25px;
        margin-bottom: 15px;

        div:first-child {
            font-weight: 200;
        }
        div:last-child {
            display: flex;
            label {
                margin-left: 15px;
                input {
                    width: 15px;
                    height: 15px;
                }
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
