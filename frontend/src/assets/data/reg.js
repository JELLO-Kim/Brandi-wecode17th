/* eslint-disable no-useless-escape */
export const idReg = /^[A-Za-z0-9][A-Za-z0-9_-]{4,20}$/
export const pwReg = /(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,20}$/
export const phReg = /^\d{3}\d{3,4}\d{4}$/
// export const nameReg = /^[ㄱ-ㅣ가-힣-0-9A-Za-z]([0-9ㄱ-ㅣ가-힣A-Za-z]){0,20}$/;
export const nameReg = /^[가-힣]+$/
export const engNameReg = /^[a-z]*$/
export const telReg = /(^02.{0}|^01.{1}|[0-9]{4})([0-9]+)([0-9]{4})/
export const urlReg = /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/
export const urlReg02 = /(http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/].[^\s]*$))?/
