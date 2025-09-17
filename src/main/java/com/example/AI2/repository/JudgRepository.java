package com.example.AI2.repository;

import com.example.AI2.entity.JudgEntity;
import com.example.AI2.entity.LawEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface JudgRepository extends JpaRepository<JudgEntity, String> {
    @Query(value = "SELECT * FROM (SELECT t.*, ROWNUM rnum FROM (SELECT * FROM hubdata0828 ORDER BY announce_date DESC) t WHERE ROWNUM <= :end) WHERE rnum > :start ORDER BY announce_date DESC", nativeQuery = true)
    List<JudgEntity> findByPage(@Param("start") int start, @Param("end") int end);

    @Query(value = "SELECT COUNT(*) FROM hubdata0828", nativeQuery = true)
    int countAll();
}
