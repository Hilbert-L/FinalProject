import { useEffect, useState } from "react";

type User = {
  id: number;
  name: string;
  active: boolean;
}

export const AdminUsers = () => {
  const [users, setUsers] = useState<User[]>();

  useEffect(() => {
    setUsers([
      {id: 0, name: "Bert Smith", active: true},
      {id: 1, name: "Bart Brown", active: false}
    ]);
  }, []);

  return (
    <div>users</div>
  );
}