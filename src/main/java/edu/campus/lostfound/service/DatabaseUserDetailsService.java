package edu.campus.lostfound.service;
import edu.campus.lostfound.repository.UserRepository;import org.springframework.security.core.userdetails.*;import org.springframework.stereotype.Service;
@Service public class DatabaseUserDetailsService implements UserDetailsService{
 private final UserRepository users;public DatabaseUserDetailsService(UserRepository users){this.users=users;}
 @Override public UserDetails loadUserByUsername(String email){var normalizedEmail=email==null?"":email.trim();var u=users.findByEmailIgnoreCase(normalizedEmail).orElseThrow(()->new UsernameNotFoundException("Account not found"));return User.withUsername(u.getEmail()).password(u.getPasswordHash()).roles(u.getRole().name()).build();}
}
