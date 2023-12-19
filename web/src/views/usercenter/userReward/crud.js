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
          },
          custom: [
          ]
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
            title: '用户ID',
            key: 'user_id',
            type: "input",
            search: true,
            show: false,
          },
          {
            title: '订单ID',
            key: 'order_id',
            type: "input",
            search: true,
            show: false,
          },
          {
            title: '被邀请ID',
            key: 'invite_user_id',
            type: "input",
            search: true,
            show: false,
          },
          {
            title: '用户',
            key: 'user_name',
            type: "input",
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '用户必填' }]
            },
            formatter (row, column, value, index) {
              return `${value}（ID:${row.user}）`
            }
          },
          {
            title: "订单号",
            key: "order_no",
            type: "input",
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '订单号必填' }]
            },
            formatter (row, column, value, index) {
              return `${value}（ID:${row.order}）`
            }
          },
          {
            title: '被邀请用户',
            key: 'invite_user',
            type: "input",
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '被邀请用户必填' }]
            },
            formatter (row, column, value, index) {
              return `${value}（ID:${row.invite_user_id}）`
            }
          },
          {
            title: '佣金',
            key: 'amount',
            type: "number",
            form: {
              component: {
                name: 'el-input-number',
                props: {
                  precision: 2
                }
              },
              scopedSlots: {
                prefix: () => '￥'
              },
              rules: [{ required: true, message: '佣金必填' }]
            }
          },
          {
            title: '下线级别',
            key: 'level',
            type: 'number',
            form: {
              component: {
                placeholder: '请输入级别',
              }
            }
          },
          {
            title: '说明',
            key: 'remark',
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
          {
            title: '创建时间',
            key: 'create_time',
            type: 'datetime',
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          }
      ]
  };
};
