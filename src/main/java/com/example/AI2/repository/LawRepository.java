package com.example.AI2.repository;

import com.example.AI2.entity.LawEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface LawRepository extends JpaRepository<LawEntity, Long> {

}
