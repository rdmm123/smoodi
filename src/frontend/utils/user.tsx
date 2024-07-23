import { User } from "services/api.types";

const getUserDisplayName = (user: User): string => {
  if (!user.name) {
    return user.email;
  }
  
  const names = user.name.split(' ');

  if (names.length <= 1) {
    return user.name;
  }

  return `${names[0]} ${names[1][0]}.`;
}

const getUserInitials = (user: User): string => {
  if (!user.name) {
    return user.email.slice(0, 2).toUpperCase();
  }

  const names = user.name.split(' ');

  return names
    .map(name => name[0].toUpperCase())
    .join('')
    .slice(0, 2);
}

export {
  getUserInitials,
  getUserDisplayName
}