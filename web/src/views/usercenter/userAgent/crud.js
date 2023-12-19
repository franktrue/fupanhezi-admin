export const crudOptions = vm => {
  return {
      pageOptions: {
          compact: true
      },
      options: {
          tableType: "vxe-table",
          rowKey: true, // 必须设置，true or false
          rowId: "id",
          height: "100%", // 表格高度100%, 使用toolbar必须设置
          highlightCurrentRow: false
      },
      rowHandle: {
          width: 140,
          view: {
              thin: true,
              text: "",
              disabled() {
                  return !vm.hasPermissions("Retrieve");
              }
          },
          edit: {
              thin: true,
              text: "",
              disabled() {
                  return !vm.hasPermissions("Update");
              }
          },
          remove: {
              thin: true,
              text: "",
              disabled() {
                  return !vm.hasPermissions("Delete");
              }
          }
      },
      indexRow: false,
      viewOptions: {
          componentType: "form"
      },
      formOptions: {
          defaultSpan: 24, // 默认的表单 span
          width: "35%"
      },
      columns: [
          {
            title: '代理ID',
            key: 'agent_id',
            type: "number",
            search: true,
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '代理ID必填' }],
              helper: "成为当前代理下线后自动成为代理并按当前设置方式进行返佣"
            }
          },
          {
            title: '下线分佣类型',
            key: 'reward_type',
            type: 'radio',
            dict: {
              data: vm.dictionary('reward_type')
            },
            form: {
              value: 'percent',
              valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
                if (value == 'percent') {
                  getColumn('reward1').title = '一级百分点'
                  getColumn('reward2').title = '二级百分点'
                  getColumn('reward3').title = '三级百分点'
                } else {
                  getColumn('reward1').title = '一级额度'
                  getColumn('reward2').title = '二级额度'
                  getColumn('reward3').title = '三级额度'
                }
              }
            },
          },
          {
            title: '分佣值',
            key: 'reward',
            type: 'input',
            form: {
              disabled: true
            },
            formatter (row, column, value, index) {
              return `${row.reward1}/${row.reward2}/${row.reward3}`
            }
          },
          {
            title: '一级百分点',
            key: 'reward1',
            type: 'number',
            show: false,
            form: {
              value: 0,
              component: {
                name: 'el-input-number',
                props: {
                  precision: 2
                }
              },
            }
          },
          {
            title: '二级百分点',
            key: 'reward2',
            type: 'number',
            show: false,
            form: {
              value: 0,
              component: {
                name: 'el-input-number',
                props: {
                  precision: 2
                }
              },
            }
          },
          {
            title: '三级百分点',
            key: 'reward3',
            type: 'number',
            show: false,
            form: {
              value: 0,
              component: {
                name: 'el-input-number',
                props: {
                  precision: 2
                }
              },
            }
          },
          {
            title: '有效期',
            key: 'end_time',
            sortable: true,
            type: 'datetime',
            form: {
              rules: [ // 表单校验规则
                { required: true, message: '有效期必填项' }
              ],
              component: {
                props: {
                  clearable: true
                },
                placeholder: '请输入有效期'
              },
            }
          },
          {
            title: '是否关闭',
            key: 'status',
            type: 'dict-switch',
            search: { disabled: false, component: { name: 'dict-select', props: { clearable: true } } },
            dict: {
              data: vm.dictionary('button_whether_number')
            },
            form: {
              value: 0,
              component: {
                props: {
                  clearable: true
                }
              },
              helper: "关闭后代理不可用"
            }
          }
      ].concat(vm.commonEndColumns())
  };
};
