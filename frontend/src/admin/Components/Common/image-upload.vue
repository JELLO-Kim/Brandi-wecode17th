<template>
  <a-upload
    name="avatar"
    list-type="picture-card"
    class="avatar-uploader"
    :show-upload-list="false"
    action="file"
    :before-upload="beforeUpload"
    :preview-file="previewFile"
    @change="handleChange"
  >
    <img v-if="imageUrl" :src="imageUrl" alt="uploadImage" class="ant-upload" />
    <div v-else>
      <a-icon :type="loading ? 'loading' : 'plus'" />
      <div class="ant-upload-text">
        Upload
      </div>
    </div>
  </a-upload>

</template>

<script>
import AdminApiMixin from '@/admin/mixins/admin-api'
import store from '@/store/index'

function getBase64 (img, callback) {
  const reader = new FileReader()
  reader.addEventListener('load', () => callback(reader.result))
  reader.readAsDataURL(img)
}
export default {
  mixins: [AdminApiMixin],
  store: store,
  data () {
    return {
      loading: false,
      imageUrl: ''
    }
  },
  props: {
    value: {
      default () {
        return ''
      }
    }
  },
  mounted () {
    this.imageUrl = this.value
  },
  computed: {
    constants () {
      return this.$store.state.const
    }
  },
  methods: {
    handleChange (info) {
      if (info.file.status === 'uploading') {
        this.loading = true
        return
      }
      if (info.file.status === 'done') {
        // Get this url from response in real world.
        getBase64(info.file.originFileObj, imageUrl => {
          this.imageUrl = imageUrl
          this.loading = false
        })
      }
    },
    beforeUpload (file) {
      const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
      if (!isJpgOrPng) {
        this.$message.error('You can only upload JPG file!')
        return false
      }
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isLt2M) {
        this.$message.error('Image must smaller than 2MB!')
        return false
      }

      if (file) {
        const formData = new FormData()
        formData.append('filename', file)
        this.post(this.constants.apiDomain + '/services/fileupload', formData).then(res => {
          this.imageUrl = res.data.result
          this.$emit('input', this.imageUrl)
        })
      }

      // 일단 모두 취소 시킴 (preview가 목적)
      getBase64(file, imageUrl => {
        this.imageUrl = imageUrl
        // this.$emit('input', file)
      })
      return false
    },
    previewFile (file) {
      console.log(file)
    }
  },
  watch: {
    value (v) {
      if (typeof (v) === 'string') { this.imageUrl = v }
    }
  }
}
</script>
<style scoped>
.avatar-uploader {
  width: auto;
}
.avatar-uploader .ant-upload {
  width: 128px;
  height: 128px;
}
.ant-upload-select-picture-card i {
  font-size: 32px;
  color: #999;
}

.ant-upload-select-picture-card .ant-upload-text {
  margin-top: 8px;
  color: #666;
}
</style>
