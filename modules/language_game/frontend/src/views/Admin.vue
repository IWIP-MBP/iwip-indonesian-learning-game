<template>
  <div class="admin-container py-4 text-white">
    <div class="d-flex justify-content-between align-items-center mb-5 flex-wrap gap-3">
      <div>
        <h1 class="display-title fw-bold mb-2 text-white glow-text-primary">KPI 培训管理后台</h1>
        <p class="text-muted fs-5">员工数据维护、考核报告导出及批量导数中心。</p>
      </div>
      
      <div>
        <button class="btn glass-btn glass-btn-primary py-3 px-4 fw-bold shadow text-white" @click="exportReport">
          📥 导出参训统计报表 (CSV)
        </button>
      </div>
    </div>

    <div class="row g-4">
      <!-- Employee Form & Import Panel -->
      <div class="col-lg-4">
        <!-- Manual Employee Add -->
        <div class="glass-card mb-4">
          <h4 class="text-white fw-bold mb-4 display-title">{{ editMode ? '编辑员工信息' : '添加参训员工' }}</h4>
          
          <form @submit.prevent="saveEmployee">
            <div class="mb-3">
              <label class="form-label text-muted small fw-medium">工号 / ID</label>
              <input 
                type="text" 
                class="form-control glass-input" 
                v-model="empForm.id" 
                placeholder="例如: EMP001" 
                :disabled="editMode"
                required
              />
            </div>
            
            <div class="mb-3">
              <label class="form-label text-muted small fw-medium">员工姓名 / NAME</label>
              <input 
                type="text" 
                class="form-control glass-input" 
                v-model="empForm.name" 
                placeholder="例如: 张三" 
                required
              />
            </div>
            
            <div class="mb-3">
              <label class="form-label text-muted small fw-medium">隶属部门 / DEPARTMENT</label>
              <select class="form-select glass-input text-white bg-dark" v-model="empForm.department_id" required>
                <option :value="null">请选择部门</option>
                <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
              </select>
            </div>
            
            <div class="mb-4">
              <label class="form-label text-muted small fw-medium">{{ editMode ? '修改密码 (留空则不修改)' : '登录密码' }}</label>
              <input 
                type="password" 
                class="form-control glass-input" 
                v-model="empForm.password" 
                placeholder="请输入密码" 
                :required="!editMode"
              />
            </div>
            
            <div class="d-flex gap-2">
              <button type="submit" class="btn glass-btn glass-btn-primary flex-grow-1 text-white fw-bold">
                {{ editMode ? '保 存' : '提 交' }}
              </button>
              <button v-if="editMode" type="button" class="btn glass-btn flex-grow-1 text-white" @click="cancelEdit">
                取 消
              </button>
            </div>
          </form>
        </div>

        <!-- Bulk JSON/Excel Import -->
        <div class="glass-card">
          <h4 class="text-white fw-bold mb-3 display-title">批量导入参训员工</h4>
          <p class="text-muted small mb-3">支持复制 Excel 表格中的 JSON 数据直接进行批量导入。</p>
          
          <div class="mb-3">
            <textarea 
              class="form-control glass-input font-monospace text-white small" 
              rows="6" 
              v-model="importJsonText"
              placeholder='[
  {"工号": "EMP010", "姓名": "李四", "部门": "生产部", "密码": "123456"},
  {"工号": "EMP011", "姓名": "王五", "部门": "后勤部", "密码": "123456"}
]'
            ></textarea>
          </div>
          
          <button class="btn glass-btn w-100 py-3 text-white fw-bold border-primary border-opacity-25 hover-bg-primary" @click="handleBulkImport">
            批量导入员工数据
          </button>
        </div>
      </div>

      <!-- Employee List Panel -->
      <div class="col-lg-8">
        <div class="glass-card">
          <h4 class="text-white fw-bold mb-4 display-title">员工信息与 KPI 列表</h4>
          
          <div class="table-responsive">
            <table class="table table-dark table-hover align-middle bg-transparent border-0">
              <thead>
                <tr class="text-muted border-bottom border-light border-opacity-10">
                  <th class="py-3 border-0">工号</th>
                  <th class="py-3 border-0">姓名</th>
                  <th class="py-3 border-0">部门</th>
                  <th class="py-3 border-0 font-monospace">等级/积分</th>
                  <th class="py-3 border-0 text-end">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="emp in employees" 
                  :key="emp.id"
                  class="border-bottom border-light border-opacity-5"
                >
                  <td class="py-3 border-0 text-white font-monospace">{{ emp.id }}</td>
                  <td class="py-3 border-0 text-white fw-medium">{{ emp.name }}</td>
                  <td class="py-3 border-0 text-muted small">{{ emp.department_name }}</td>
                  <td class="py-3 border-0 text-success small font-monospace">LV.{{ emp.level }} ({{ emp.xp }} XP)</td>
                  <td class="py-3 border-0 text-end">
                    <button class="btn btn-sm btn-outline-info me-2 border-0" @click="editEmployee(emp)">编辑</button>
                    <button class="btn btn-sm btn-outline-danger border-0" @click="deleteEmployee(emp.id)" :disabled="emp.id === 'admin'">删除</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const employees = ref([])
const departments = ref([
  { id: 1, name: '管理层' },
  { id: 2, name: '行政部' },
  { id: 3, name: '安全环保部' },
  { id: 4, name: '生产部' },
  { id: 5, name: '设备部' },
  { id: 6, name: '后勤部' }
])

const empForm = ref({
  id: '',
  name: '',
  department_id: null,
  password: '',
  role: 'employee'
})

const editMode = ref(false)
const importJsonText = ref('')

const fetchEmployees = async () => {
  try {
    const response = await axios.get('/api/admin/employees')
    employees.value = response.data
  } catch (err) {
    console.error('Failed to load employees list:', err)
  }
}

const saveEmployee = async () => {
  try {
    if (editMode.value) {
      await axios.put(`/api/admin/employees/${empForm.value.id}`, empForm.value)
      alert('员工信息修改成功')
    } else {
      await axios.post('/api/admin/employees', empForm.value)
      alert('员工添加成功')
    }
    cancelEdit()
    fetchEmployees()
  } catch (err) {
    alert(err.response?.data?.message || '操作失败')
  }
}

const editEmployee = (emp) => {
  editMode.value = true
  empForm.value = {
    id: emp.id,
    name: emp.name,
    department_id: emp.department_id,
    password: '',
    role: emp.role
  }
}

const cancelEdit = () => {
  editMode.value = false
  empForm.value = {
    id: '',
    name: '',
    department_id: null,
    password: '',
    role: 'employee'
  }
}

const deleteEmployee = async (id) => {
  if (confirm(`确定要删除工号为 ${id} 的员工吗？此操作无法撤销。`)) {
    try {
      await axios.delete(`/api/admin/employees/${id}`)
      fetchEmployees()
    } catch (err) {
      alert('删除失败')
    }
  }
}

const handleBulkImport = async () => {
  if (!importJsonText.value.strip) {
    // Basic trim check
    if (!importJsonText.value.trim()) {
      alert('请输入JSON数据')
      return
    }
  }
  
  try {
    const data = JSON.parse(importJsonText.value)
    const response = await axios.post('/api/admin/employees/import-json', data)
    alert(response.data.message)
    importJsonText.value = ''
    fetchEmployees()
  } catch (err) {
    alert('JSON格式错误或导入失败：' + err.message)
  }
}

const exportReport = async () => {
  try {
    // Direct file download trigger via browser window location or axios blob
    const response = await axios.get('/api/admin/reports/export', { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'employees_learning_report.csv')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (err) {
    alert('报表导出失败')
  }
}

onMounted(() => {
  fetchEmployees()
})
</script>

<style scoped>
.hover-bg-primary:hover {
  background: rgba(99, 102, 241, 0.15) !important;
  border-color: var(--color-primary) !important;
}

.table th {
  font-weight: 600;
  font-size: 13px;
}

.table tr {
  transition: background-color 0.2s ease;
}

.table-hover tbody tr:hover {
  background-color: rgba(255, 255, 255, 0.03) !important;
}
</style>
