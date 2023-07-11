import { request } from '@/api/service'
import { urlPrefix as subjectPrefix } from './api'
import XEUtils from 'xe-utils'
export const crudOptions = (vm) => {
  return {
    pagination: false,
    pageOptions: {
      compact: true
    },
    options: {
      tableType: 'vxe-table',
      rowKey: true,
      rowId: 'id',
      height: '100%', // 表格高度100%, 使用toolbar必须设置
      highlightCurrentRow: false,
      // defaultExpandAll: true,
      // expandAll: true,
      treeConfig: {
        transform: true,
        rowField: 'id',
        parentField: 'parent',
        expandAll: true,
        hasChild: 'hasChild',
        lazy: true,
        loadMethod: vm.loadContentMethod
      }
    },
    rowHandle: {
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      },
      width: 240,
      fixed: 'right',
      custom: [{
        disabled () {
          return !vm.hasPermissions('Fetch')
        },
        text: ' 成分股',
        type: 'success',
        size: 'small',
        icon: 'el-icon-folder',
        emit: 'subjectCons'
      }]

    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 80
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 12 // 默认的表单 span
    },
    columns: [
      {
        title: 'ID',
        key: 'id',
        show: false,
        width: 60,
        form: {
          component: {
            show: false
          }
        }
      },
      {
        title: '父级菜单',
        key: 'parent',
        show: false,
        search: {
          disabled: true
        },
        type: 'cascader',
        dict: {
          url: subjectPrefix,
          cache: false,
          isTree: true,
          value: 'id', // 数据字典中value字段的属性名
          label: 'name', // 数据字典中label字段的属性名
          children: 'children', // 数据字典中children字段的属性名
          getData: (url, dict, { form, component }) => { // 配置此参数会覆盖全局的getRemoteDictFunc
            return request({ url: url, params: {limit:9999}}).then(ret => {
              const responseData = ret.data.data
              console.log(responseData)
              const result = XEUtils.toArrayTree(responseData, { parentKey: 'parent', strict: true })
              return [{ id: null, name: '根节点', children: result }]
            })
          }
        },
        form: {
          component: {
            props: {
              elProps: {
                clearable: true,
                showAllLevels: false, // 仅显示最后一级
                props: {
                  checkStrictly: true, // 可以不需要选到最后一级
                  emitPath: false,
                  clearable: true
                }
              }
            }
          }
        }
      },
      {
        title: '题材名称',
        key: 'name',
        sortable: true,
        treeNode: true, // 设置为树形列
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        minWidth: 180,
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '题材名称必填项' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入题材名称'
          },
          itemProps: {
            class: { yxtInput: true }
          }

        }
      },
      {
        title: '题材代码',
        key: 'code',
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        form: {
          rules: [
            { required: true, message: '请输入题材代码' }
          ],
          component: {
            show (context) {
              const { form } = context
              return !form.is_catalog && !form.is_link
            },
            props: {
              clearable: true
            },
            placeholder: '请输入题材代码'
          }
        },
        valueResolve(row, key) {
          row.id = row.code
        }
      },
      {
        title: '层级',
        key: 'level',
        type: 'number',
        show: false,
        form: {
          value: 1,
          component: {
            placeholder: '请输入层级'
          }
        }
      },
      {
        title: '说明',
        key: 'desc',
        minWidth: 500,
        type: 'textarea',
        form: {
          component: {
            placeholder: '请输入说明',
            showWordLimit: true,
            maxlength: '500',
            props: {
              type: 'textarea'
            }
          }
        }
      },
    ]
  }
}
