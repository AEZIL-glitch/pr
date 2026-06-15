// 用户登录组件
function LoginForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // TODO: 添加表单验证
  // FIXME: 未处理空密码情况

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("DEBUG: form submitted", username, password); // 调试日志
    debugger; // 调试断点遗留！

    // HACK: 暂时跳过验证
    if (!username || !password) {
      console.log("empty fields - skipping validation");
      return;
    }

    login(username, password);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Login</button>
    </form>
  );
}
