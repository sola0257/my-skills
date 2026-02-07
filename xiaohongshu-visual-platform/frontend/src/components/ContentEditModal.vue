<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h2>编辑内容</h2>
        <button class="close-btn" @click="$emit('close')">×</button>
      </div>

      <div class="modal-body">
        <div class="form-group">
          <label>标题</label>
          <input
            v-model="editedContent.title"
            type="text"
            class="form-input"
            placeholder="请输入标题"
          >
        </div>

        <div class="form-group">
          <label>正文</label>
          <textarea
            v-model="editedContent.body"
            class="form-textarea"
            rows="15"
            placeholder="请输入正文内容"
          ></textarea>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-secondary" @click="$emit('close')">
          取消
        </button>
        <button class="btn btn-primary" @click="handleSave">
          保存修改
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  content: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'save'])

const editedContent = ref({
  title: props.content.title,
  body: props.content.body
})

function handleSave() {
  emit('save', editedContent.value)
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
</style>
